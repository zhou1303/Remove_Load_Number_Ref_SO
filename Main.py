import Post_Data
import Constant
import time
import G_API
import Get_Data
import json
import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy


if __name__ == '__main__':

    # START COUNTING RUNNING TIME
    start = time.time()

    count = 0

    # LOGIN TMS
    Get_Data.read_login_credentials()
    Get_Data.read_report_oid()
    session_requests, csrf = Post_Data.login_tms()

    # Concatenate for route board report url.
    url_report_routeboard = Constant.url_report_routeboard
    url_report_routeboard = url_report_routeboard.replace('OID_TO_REPLACE', str(Constant.oid_report_so))

    # Request route board report.
    print('Reading data from route board...')
    response = session_requests.get(url_report_routeboard).text
    # Convert json_response.
    route_board_json_responses = json.loads(response)
    print('Route board data read successfully.')

    # Dictionaries for customer loads and execution loads.
    so_dict = Get_Data.get_so_info(session_requests, route_board_json_responses)
    # Get OIDs and corresponding load numbers.
    el_dict = Get_Data.get_load_number_by_oid(session_requests, csrf, so_dict)

    # Create lists to record removals.
    rm_load = list()
    rm_so = list()

    # Run through SOs and remove Ref: Load Number if EL is not attached to SO.
    print('Checking Ref: Load Number\'s match to execution load...')
    for so_oid, so_info in so_dict.items():
        el_oids = so_info['executionLoadOids']

        # Look into ELs attached to the SO, find the load numbers on SO.
        load_number_on_so = [el_dict[i] for i in el_oids]

        # Run through Ref: Load Number and remove if not matching load number attached.
        load_number_ref_value = so_info['refLoadNumber']
        load_number_ref_oid = so_info['refLoadNumberOid']
        route_oid = so_info['routeOid']
        so_pri_ref = so_info['primaryReference']
        for i, value in enumerate(load_number_ref_value):
            if value not in load_number_on_so:
                Post_Data.delete_ref_load_number(session_requests, so_oid, load_number_ref_oid[i], csrf)
                count += 1
                rm_load.append(value)
                rm_so.append(so_pri_ref)
                print('Ref: Load Number', value, 'has been removed from SO', so_pri_ref, '.')
    Post_Data.save_removal_in_xlsx(rm_load, rm_so)
    print(str(count), 'references have been removed.')
    print('Process is completed and will be logged. This window will be closed automatically in 30 seconds.')

    # END TIME
    end = time.time()

    # UPDATE LOG REPORT ON GOOGLE SHEETS
    duration = end - start
    workbook_log = G_API.get_workbook_by_id(Constant.g_sheets_workbook_id_log)
    worksheet_log = G_API.get_worksheet_by_id(workbook_log, Constant.g_sheets_worksheet_id_log)
    Post_Data.log_event(worksheet_log, duration)

    time.sleep(30)

# save_file = open(Constant.root_path + 'test.html', 'w+')
# save_file.write(html_script)
# save_file.close()