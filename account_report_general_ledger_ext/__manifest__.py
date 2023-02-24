# -*- coding: utf-8 -*-
{
    'name': "account report general ledger ext",
    'summary': """
        The general ledger shows foreign currency amount
    """,
    'description': """
    总账显示外币金额
    The general ledger shows foreign currency amount
    """,
    'author': "zero",
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['base', 'account', 'account_reports'],
    'data': [
        # 'security/ir.model.access.csv',
    ],
    'qweb': [
    ],
    'images': [
        'static/description/icon.png',
        'static/description/main_screenshot.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
