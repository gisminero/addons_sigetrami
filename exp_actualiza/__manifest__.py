# -*- coding: utf-8 -*-
{
    'name': "SIGETRAMI Actualización desde versión anterior.",

    'summary': """
        Consulta la base de datos del sistema en su versón a anterior para actualizar el actual.""",

    'description': """
Consulta un sistema anterior instalado cada 5 minutos, para mantener actualizada la versiòn actual.
    """,

    'author': "GIS Minero Nacional",
    'website': "http://www.gismineronacional.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Actualización desde version anterior.',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['tarea', 'expediente', 'hr', 'mail', 'base'],

    # always loaded
    'data': [
        #'security/notificaciones_security.xml',
        #'security/ir.model.access.csv',
        #'views/views.xml',
        'data/auto_server.xml',
        #'data/ini.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': True,
}