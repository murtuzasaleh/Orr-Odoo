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
        'data/visit_cron.xml',
        'views/contract_template.xml',
        'views/contract.xml',
        'views/contract_line.xml',
        'views/recurrence_recurrence.xml',
        'views/sale_order_frequency.xml',
        'views/visit_visit.xml',
        'views/sale_order_view.xml',
    ],
    'maintainers': [
        'smangukiya',
    ],
    "installable": True,
    "post_init_hook": "_deactivate_contract_cron",
}
