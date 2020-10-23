# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractAbstractContract(models.AbstractModel):
    _inherit = "contract.abstract.contract"

    advance_number = fields.Integer(
        string="Days to Create SO in Advance",
        default=60
    )
    billing_partner_id = fields.Many2one(
        "res.partner", string="Billing Customer"
    )
    min_bill_hours = fields.Float(string="Minimum Billable Hours")
    per_visit_amt_restriction = fields.Float(
        string="Not to Exceed Total Amount Per Visit")
    default_analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Default Analytic Account"
    )
    default_analytic_account_tag_id = fields.Many2one(
        "account.analytic.tag", string="Default Analytic Tags"
    )
    fsm_notes = fields.Text(string="General FSM Notes")
    contract_type = fields.Selection(
        selection=[('sale', 'Sale Order'), ('purchase', 'Supplier')],
        default='sale',
        index=True,
    )
    type = fields.Selection(
        [('invoice', 'Invoice'),
         ('sale', 'Sale')],
        string='Type',
        default='sale',
    )
    sale_autoconfirm = fields.Boolean(
        string='Sale Autoconfirm',
        default=True)
