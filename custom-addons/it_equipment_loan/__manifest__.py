{
    'name': "It Equipment Loan",
    'version': '19.0.1',
    'sequence': -99,
    'category': 'Service',
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
        Projet de module Odoo 19 pour gérer le prêt de matériel informatique. Le nom technique prévu pour le module est `it_equipment_loan`
    """,
    'author': 'Bayz225',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr'],

    # always loaded
    'data': [
        # 1. Sécurités
        'security/ir.model.access.csv',
        
        # 2. Données
        "data/ir_sequence.xml",
        
        # 3. Vues de l'interface
        'views/menu.xml',
        'views/it_equipment_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'it_equipment_loan/static/src/scss/style.scss',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True, # Permet au module d'apparaître dans l'écran principal des Apps
    'license': 'LGPL-3',
}

