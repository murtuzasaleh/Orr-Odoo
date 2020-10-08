# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ContractAbstractContract(models.AbstractModel):
    _inherit = "contract.abstract.contract"

    advance_number = fields.Integer(
        string="Days to create SOs in advance",
        default=60
    )
    billing_partner_id = fields.Many2one(
        "res.partner", string="Billing Customer"
    )
    min_bill_hours = fields.Float(string="Minimum billable hours")
    per_visit_amt_restriction = fields.Float(
        string="Not to exceed total amount per visit")
    default_analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Default Analytic Account"
    )
    default_analytic_account_tag_id = fields.Many2one(
        "account.analytic.tag", string="Default Analytic Tags"
    )
    fsm_notes = fields.Text(string="General FSM Notes")
