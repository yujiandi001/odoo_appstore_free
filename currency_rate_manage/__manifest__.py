# -*- coding: utf-8 -*-
{
    'name': "Currency Rate Manage",
    'summary': """
        Manage the same exchange rate for multiple companies
    """,
    'description': """
        Manage the same exchange rate for multiple companies
        可以选择多个公司，一键创建多条相同日期相同汇率的数据
        
    """,
    'author': "zero",
    'category': 'Accounting/Accounting',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/currency_rate_manage.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    # 'post_init_hook': 'load_translations',
}
