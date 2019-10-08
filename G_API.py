from oauth2client.service_account import ServiceAccountCredentials
import gspread


scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('dsc_tmc_gsheets_api_service_account_credentials.json',
                                                               scope)
client = gspread.authorize(credentials)


def get_workbook_by_id(workbook_id):
    return client.open_by_key(workbook_id)


def get_worksheet_by_id(workbook, worksheet_id):
    for i, worksheet in enumerate(workbook.worksheets()):
        if worksheet.id == worksheet_id:
            return worksheet
    return None


def get_values_in_list(worksheet):
    return worksheet.get_all_values()


def get_values_in_dict(workbook_id, worksheet_id, empty2zero=False, head=1, default_blank='',
                       allow_underscores_in_numeric_literals=False):
    worksheet = get_worksheet_by_id(workbook_id, worksheet_id)
    return worksheet.get_all_records(empty2zero, head, default_blank,
                                     allow_underscores_in_numeric_literals)


def get_next_available_row(worksheet, col_index):
    return len(worksheet.col_values(col_index))+1


def convert_values_to_dict(values):
    data_dict = dict()
    #ADD EMPTY STRING TO HAVE LISTS HAD SAME LENGTH
    n = len(values[0])
    for i, value in enumerate(values):
        while len(values[i]) != n:
            values[i].append('')
    values = list(map(list, zip(*values))) #Transpose list.

    for value in values:
        data_dict[value[0]] = [item for item in value[1:] if item != '']

    #REMOVE DICT ITEM IF ALL ELEMENTS ARE EMPTY STRING
    for key, item in data_dict.copy().items():
        is_all_empty_string = True
        for list_item in item:
            if list_item != '':
                is_all_empty_string = False
                break
        if is_all_empty_string:
            del data_dict[key]
    return data_dict


