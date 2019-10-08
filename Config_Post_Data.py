import Constant


def config_ref_del(so_oid, ref_oid):
    data_dict = Constant.data_dict_ref_del.copy()
    data_dict['ownerOid'] = so_oid
    data_dict['referenceOid'] = ref_oid
    return data_dict


def config_transport_find_pri_ref(csrf, oids):
    data_dict = Constant.transport_by_report_format_dict.copy()
    data_dict['_csrf'] = csrf

    data_dict['filterfield0'] = Constant.field_oid
    data_dict['filtercrit0'] = Constant.filter_in
    data_dict['filtervalue0'] = ','.join(str(oid) for oid in oids)

    return data_dict
