import Constant
import Config_Post_Data
import requests
import time
from datetime import datetime
import G_API
import pandas as pd


def login_tms():

    login_info = {
        'UserId': Constant.login_userid,
        'Password': Constant.login_password,
        'RememberMe': 'true',
        'submitbutton': '++++Sign+In++++',
        'NoAutoLogin': 'true',
        'menus': 'top',
        'inline': 'true'
    }

    session_requests = requests.session()

    response = session_requests.post(
        Constant.url_tms_login,
        data=login_info,
    )

    csrf = Constant.re_pattern_csrf.search(response.text).group(1)

    print('Login as', Constant.login_userid, '...')
    print('Login to TMS successfully.')

    return session_requests, csrf


def log_event(worksheet, duration):

    now = datetime.fromtimestamp(time.time()).strftime(Constant.time_format_military)

    titles = worksheet.get_all_values()[0]
    titles_dict = dict()
    for i, title in enumerate(titles):
        titles_dict[title] = i + 1

    next_row = G_API.get_next_available_row(worksheet, 1)

    worksheet.update_cell(next_row, titles_dict['Process'], Constant.process_name)
    worksheet.update_cell(next_row, titles_dict['Log By'], Constant.login_userid)
    worksheet.update_cell(next_row, titles_dict['Log Time'], now)
    worksheet.update_cell(next_row, titles_dict['Duration'], duration)


def delete_ref_load_number(session_requests, so_oid, ref_oid, csrf):
    data_dict = Config_Post_Data.config_ref_del(so_oid, ref_oid)
    header = {
        'X-CSRF-TOKEN': csrf
    }
    session_requests.post(
        url=Constant.url_reference_delete,
        data=data_dict,
        headers=header
    )


def save_removal_in_xlsx(rm_load, rm_so):
    print('Saving removal log into Excel file...')
    rm_load = pd.DataFrame(rm_load, columns=['Ref: Load Number'])
    rm_so = pd.DataFrame(rm_so, columns=['BOL'])
    rm = pd.concat([rm_so, rm_load], axis=1)

    writer = pd.ExcelWriter(Constant.xlsx_file_name_rm_log + str(int(time.time())) + '.xlsx', engine='xlsxwriter')
    rm.to_excel(writer, index=False)
    writer.save()
    writer.close()
    print('Log saved successfully.')
