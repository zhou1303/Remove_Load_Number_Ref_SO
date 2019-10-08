import Constant
import json
import Config_Post_Data


def read_login_credentials():
    login_userid = open('username.txt', mode='r')
    login_password = open('password.txt', mode='r')

    Constant.login_userid = login_userid.read()
    Constant.login_password = login_password.read()

    print('User credentials read successfully.')


def read_report_oid():
    report_oid = open('report_oid.txt', mode='r')
    Constant.oid_report_so = report_oid.read()
    print('Report OID read successfully.')


def get_transport_report_by_report_format(session_requests, data_dict):
    response = session_requests.post(
        Constant.url_post_transport_report_format,
        data_dict
    )

    html_script = response.text
    urls = Constant.re_pattern_url_transport_report_format.findall(html_script)
    for url in urls:
        session_requests.get(Constant.url_tms_root + url)

    response = session_requests.get(Constant.url_get_transport_report_format0)
    html_script = response.text
    urls = Constant.re_pattern_url_transport_report_format.findall(html_script)
    for url in urls:
        session_requests.get(Constant.url_tms_root + url)

    response = session_requests.get(Constant.url_get_transport_report_format1)
    return response


def get_so_info(session_requests, route_board_json_responses):
    # Dictionaries for customer loads and execution loads.
    so_dict = dict()
    print('Querying each shipping order\'s information...')
    for route_board_json_response in route_board_json_responses:
        # Customer loads' information.
        sos = route_board_json_response['customerLoads']
        for so in sos:
            # Get information from route board query.
            so_oid = so['oid']
            route_oid = so['routeOid']
            el_on_so_oids = so['executionLoadOids']
            pri_ref_so = so['primaryReference']['name']

            # Get reference information from SO query.
            url_reference_value = Constant.url_reference_value.replace('TRANSPORT_OID_TO_REPLACE', str(so_oid))
            url_reference_value = url_reference_value.replace('REF_OID_TO_REPLACE',
                                                              str(Constant.oid_ref_load_number))
            so_ref_json_response = json.loads(session_requests.get(url_reference_value).text)
            ref_value_so = [i['name'] for i in so_ref_json_response['references']]
            ref_oid_so = [i['oid'] for i in so_ref_json_response['references']]

            so_dict[so_oid] = {
                'routeOid': route_oid,
                'executionLoadOids': el_on_so_oids,
                'primaryReference': pri_ref_so,
                'refLoadNumber': ref_value_so,
                'refLoadNumberOid': ref_oid_so
            }
    print('Shipping order information collected successfully.')
    return so_dict


def get_load_number_by_oid(session_requests, csrf, so_dict):
    # Use set to collect OIDs since there will be duplicate.
    el_oids = set()
    # Get a list of execution loads' oids.
    for key, value in so_dict.items():
        for execution_load_oid in value['executionLoadOids']:
            el_oids.add(execution_load_oid)
    # Convert set into a list object.
    el_oids = list(el_oids)
    # Split the list into groups with each of them has no more than 100 loads.
    n = 100
    el_oid_lists = [el_oids[i * n:(i + 1) * n] for i in range((len(el_oids) + n - 1) // n)]
    # Request report to TMS and get responses in HTML.
    html_script = ''
    for el_oid_list in el_oid_lists:
        data_dict = Config_Post_Data.config_transport_find_pri_ref(csrf, el_oid_list)
        response = get_transport_report_by_report_format(session_requests, data_dict)
        html_script += response.text
    # Parse response data, get oid and corresponding load numbers.
    oids = Constant.re_pattern_transport_oid.findall(html_script)
    load_numbers = Constant.re_pattern_transport_pri_ref.findall(html_script)

    assert len(oids) == len(load_numbers), 'Error: Found different numbers of OIDs and Load Numbers!'

    # Put OIDs and load numbers together and make a dictionary to return.
    el_dict = dict()
    for i, oid in enumerate(oids):
        el_dict[int(oid)] = load_numbers[i]

    return el_dict
