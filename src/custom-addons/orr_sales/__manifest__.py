# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services Pvt. Ltd.
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
