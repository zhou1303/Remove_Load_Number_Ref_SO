import re

root_path = 'C:\\Users\\Zhou_Charles\\Desktop\\'

login_userid = None
login_password = None

time_format_military = '%m/%d/%Y %H:%M'
process_name = 'Remove_Load_Number_Ref_SO'
g_sheets_workbook_id_log = '1Yudm7JfKSgL82zyHXnDKUjJfoI5VGoEsPHgysPXcZ4g'
g_sheets_worksheet_id_log = 0

url_tms_login = 'https://dsclogistics.mercurygate.net/MercuryGate/login/LoginProcess.jsp'
url_tms_root = 'https://dsclogistics.mercurygate.net'
url_report_routeboard = 'https://dsclogistics.mercurygate.net/MercuryGate/rest/routes/?isDynamic=false&configGroupId=' \
                        'OPSSupervisorezVision&reportOid=OID_TO_REPLACE&isHistorical=false'
url_reference_value = 'https://dsclogistics.mercurygate.net/MercuryGate/rest/routes/identityColumn?transportOid=' \
                      'TRANSPORT_OID_TO_REPLACE&refTypes=REF_OID_TO_REPLACE'
url_reference_delete = 'https://dsclogistics.mercurygate.net/MercuryGate/extJsPortletAction/action.referencedelete'
url_route_board_detail = 'https://dsclogistics.mercurygate.net/MercuryGate/mgreact/reactMultiWindowController.jsp#/' \
                     'ROUTE_OID_TO_REPLACE/references/?selectedLoadOid=TRANSPORT_OID_TO_REPLACE'

url_post_transport_report_format = 'https://dsclogistics.mercurygate.net/MercuryGate/report/ReportFormat_process.jsp?' \
                              'type=Transport&summary=false'
url_get_transport_report_format0 = 'https://dsclogistics.mercurygate.net/MercuryGate/transport/listTransports.jsp?' \
                                   'sidAction=&action=&type=Transport&full=&nSetNumber=1&sReturnURL='
url_get_transport_report_format1 = 'https://dsclogistics.mercurygate.net/MercuryGate/transport/listTransports.jsp?' \
                                   'norefresh=&sidAction=&action=&type=Transport&full=&nSetNumber=1&sReturnURL='

re_pattern_csrf = re.compile('\<meta name\=\"_csrf\" content\=\"([\w\-]*)\" \/\>')
re_pattern_menu_value = re.compile('\<a href\=\"\.\.\/mainframe\/menuLHS\.jsp\?sMenuValue\=([\d\(\)\,]*)'
                                  '\&sMenuSelected\=\*\-\%3EDetail')
re_pattern_script_url = re.compile('\<script src\=\"([\/\w\-\.\?\=\_\&]+)\" type\=\"text\/javascript\"\>\<\/script\>')
re_pattern_url_transport_report_format = re.compile('\<script src\=\"([\/\w\.\?\=]*)\"')
re_pattern_transport_pri_ref = re.compile('Primary Reference\' class\=\"DetailBodyTableRowOdd \"\>([\w\-]+) \(Load Number\)')
re_pattern_transport_oid = re.compile('OID\' class\=\"DetailBodyTableRowOdd \"\>(\d{11})\<\/td\>')

oid_ref_load_number = 1174978200 # Ref: Load Number request oid.
oid_enterprise = 54775198209 # ezVision
oid_report_so = None # 99 - Load Number Ref Cleaning

html_equivalence_and = '&amp;'

field_oid = 'Oid'

filter_equal = 'Equal'
filter_in = 'In'
filter_not_in = 'Not In'
filter_not_equal = 'Not Equal'
filter_from_today = 'From Today'
filter_begins_with = 'Begins With'
filter_not_begins_with = 'Not Begin With'

xlsx_file_name_rm_log = 'Removal Log'

data_dict_ref_del = {
    'ownerOid': '',
    'ownerType': '3300',
    'referenceOid': '',
    'requireApproval': '',
    'changeRequestOwnerOid': '',
    'changeRequestType': ''
}


transport_by_report_format_dict = {
    '_csrf': '',
    'sourceurl': '',
    'sReturnURL': '',
    'full': '',
    'action': '     Use     ',
    'col0': 'Oid',
    'col1': 'PrimaryReference',
    'filterfield0': '', 'filtercrit0': '', 'filtervalue0': '',
    'filterfield1': '', 'filtercrit1': '', 'filtervalue1': '',
    'filterfield2': '', 'filtercrit2': '', 'filtervalue2': '',
    'filterfield3': '', 'filtercrit3': '', 'filtervalue3': '',
    'filterfield4': '', 'filtercrit4': '', 'filtervalue4': '',
    'filterfield5': '', 'filtercrit5': '', 'filtervalue5': '',
}
