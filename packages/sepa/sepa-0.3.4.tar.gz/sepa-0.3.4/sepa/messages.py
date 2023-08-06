from .general import code_or_proprietary, group_header, party
from .payment import payment_group_header, payment
from .mandate import mandate

def original_message(tag):
    return {
        '_self': tag,
        '_sorting': ['MsgId', 'MsgNmId', 'CreDtTm'],
        'message_id': 'MsgId',
        'message_name_id': 'MsgNmId',
        'creation_date_time': 'CreDtTm'
    }

customer_direct_debit_initiation = {
    '_namespaces': {
        None: 'urn:iso:std:iso:20022:tech:xsd:pain.008.001.07',
        'xs': 'http://www.w3.org/2001/XMLSchema'
    },
    '_self': 'CstmrDrctDbtInitn',
    '_sorting': ['GrpHdr', 'PmtInf', 'SplmtryData'],
    'group_header': payment_group_header('GrpHdr'),
    'payments': [payment('PmtInf')],
    'supplementary_data': ['SplmtryData']
}

mandate_initation_request = {
    '_namespaces': {
        None: 'urn:iso:std:iso:20022:tech:xsd:pain.009.001.05',
        'xs': 'http://www.w3.org/2001/XMLSchema'
    },
    '_self': 'MndtInitnReq',
    '_sorting': ['GrpHdr', 'Mndt', 'SplmtryData'],
    'group_header': group_header('GrpHdr'),
    'mandate': [mandate('Mndt')],
    'supplementary_data': ['SplmtryData']
}

mandate_amendment_request = {
    '_namespaces': {
        None: 'urn:iso:std:iso:20022:tech:xsd:pain.010.001.05',
        'xs': 'http://www.w3.org/2001/XMLSchema'
    },
    '_self': 'MndtAmdmntReq',
    '_sorting': ['GrpHdr', 'UndrlygAmdmntDtls', 'SplmtryData'],
    'group_header': group_header('GrpHdr'),
    'amendment': [{
        '_self': 'UndrlygAmdmntDtls',
        'original_message': original_message('OrgnlMsgInf'),
        'reason': {
            '_self': 'AmdmntRsn',
            'originator': party('Orgtr'),
            'reason': code_or_proprietary('Rsn'),
            'additional_information': ['AddtInf']
        },
        'mandate': mandate('Mndt'),
        'original_mandate': {
            '_self': 'OrgnlMsgInf',
            'id': 'OrgnlMndtId',
            'mandate': mandate(' OrgnMndt')
        },
        'supplementary_data': ['SplmtryData']
    }],
    'supplementary_data': ['SplmtryData']
}

mandate_cancellation_request = {
    '_namespaces': {
        None: 'urn:iso:std:iso:20022:tech:xsd:pain.011.001.05',
        'xs': 'http://www.w3.org/2001/XMLSchema'
    },
    '_self': 'MndtCxlReq',
    '_sorting': ['GrpHdr', 'UndrlygCxlDtls', 'SplmtryData'],
    'group_header': group_header('GrpHdr'),
    'cancellatiion': [{
        '_self': 'UndrlygCxlDtls',
        'original_message': original_message('OrgnlMsgInf'),
        'reason': {
            '_self': 'CxlRsn',
            'originator': party('Orgtr'),
            'reason': code_or_proprietary('Rsn'),
            'additional_information': ['AddtInf']
        },
        'original_mandate': {
            '_self': 'OrgnlMsgInf',
            'id': 'OrgnlMndtId',
            'mandate': mandate(' OrgnMndt')
        },
        'supplementary_data': ['SplmtryData']
    }],
    'supplementary_data': ['SplmtryData']
}
