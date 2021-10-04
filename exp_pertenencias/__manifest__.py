# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI - Cantidad de pertenencias",

    'summary': """
        Registro de pertenencias""",

    'description': """
       Registro de cantidad de pertenencias por expediente
    """,

    'author': "Secretaría de minería",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'expediente'], #agrego los models con los que se relaciona en este caso expediente

    # always loaded
    'data': [
        'security/accesos_pertenencias.xml',
        'security/ir.model.access.csv',
        'views/views_over.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True
}
