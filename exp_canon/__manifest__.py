# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI - Pago de Canon Minero",

    'summary': """
        Calculo y Registro de pago de canon minero.""",

    'description': """
        Cálculo y registro de pago de canon minero.
    """,

    'author': "Secretaria de Mineria",
    'website': "http://www.gismineronacional.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'expediente', 'sh_message'],
    # always loaded
    'data': [
        'security/canon_security.xml',
        'security/ir.model.access.csv',
        'views/views_canon_over.xml',
        'views/config_general_canon.xml',
        'views/config_valor_general.xml',
        'views/popup_informa_pago.xml',
        'data/config_default.xml',
        'data/cronos_vencimientos.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}