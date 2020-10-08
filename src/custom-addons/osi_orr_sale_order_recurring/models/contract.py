# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    is_po_required = fields.Boolean(
        string="PO required"
    )
    po_number = fields.Char(
        string="PO Number"
    )
    service_start_date = fields.Date(
        string="Service Start date", required=True)
    service_end_date = fields.Date(
        string="Service End date")
    old_contract_id = fields.Many2one(
        'contract.contract', string='Copied from')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('active', 'Active'),
         ('expired', 'Expired')],
        string="State",
    )
    initial_sale_id = fields.Many2one(
        'sale.order', string='Initial sale order')
