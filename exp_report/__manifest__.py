# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI Reportes",

    'summary': """
        Reportes de Sistema""",

    'description': """
        Reportes básicos del sistema SIGETRAMI
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','gepromi', 'expediente'],

    # always loaded
    'data': [
        'security/report_security.xml',
        'security/ir.model.access.csv',
        'views/views_exp_report.xml',
        #'views/templates.xml',
        # 'data/departamentos_arg.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'application': True,
    'auto_install': True,
}