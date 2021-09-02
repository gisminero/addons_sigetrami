{ 
    'name': 'SIGETRAMI - Inversión de capital', 
    'summary': """
        Registro de inversión de capital.""",
    'description': """
       Registro de inversión de capital.
    """,

    'author': "Secretaria de Mineria",
    'website': "http://www.gismineronacional.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'expediente', 'sh_message'],
    'data': [
        'security/inv_capital_security.xml',
        'security/ir.model.access.csv',
        'views/view_inversion_de_capital.xml'
    ],

    'application': True, 
}