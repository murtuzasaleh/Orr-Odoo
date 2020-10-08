# Copyright (C) 2020 Open Source Integrators
# Copyright (C) 2020 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'OSI ORR Sale Order Recurring',
    'summary': 'This module will create Recurring SO from Contract',
    'license': 'AGPL-3',
    'version': '12.0.1.0.0',
    'category': 'Field Service',
    'author': 'Open Source Integrators',
    'depends': [
        'contract_sale_generation',
        'fieldservice',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'maintainers': [
        'smangukiya',
    ],
    "installable": True,
}
