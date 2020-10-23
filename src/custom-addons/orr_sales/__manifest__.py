# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'ORR Sale',
    'author': 'ORR Dev trg',
    'depends': [
        'sale',
        'contacts'
    ],
    'application': False,
    'installable': True,
    'data': [
        'views/res_partner.xml',
        'views/product.xml',
    ]
}
