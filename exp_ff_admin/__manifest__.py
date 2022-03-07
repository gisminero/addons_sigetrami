# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI - Administración de Expedientes Fuera de Flujos",

    'summary': """
        Funcionalidad de Administracion de Expedientes cuando se encuentran fuera de flujo.""",

    'description': """
        Permite relizar la gestión de expedientes enviandolos por oficina, cuando se encuentran fuera de flujo preestablecido.
    """,

    'author': "Gis Minero Nacional",
    'website': "http://www.gismineronacional.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'expediente', 'sh_message', 'pase', 'tarea_flujo_exp'],
    # always loaded
    'data': [
        'security/ff_security.xml',
        'security/ir.model.access.csv',
        'views/exp_over.xml',
        #'views/exp_correcc_flujo.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}