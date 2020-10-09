# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrderFrequencyLine(models.Model):
    _name = "sale.order.frequency.line"
    _description = "SO Frequency Line"

    sequence = fields.Integer(
        string="Sequence")
    recurrence_id = fields.Many2one(
        "recurrence.recurrence", string="Recurrence"
    )
    recurrence_ids = fields.Many2many(
        "recurrence.recurrence", string="Exclude"
    )
    visit_type = fields.Selection(
        [("full", "Full"),
         ("medium", "Medium"),
         ("small", "Small")],
        string="Visit Type",
    )
    hours = fields.Float(string="Hours")
    unit_price = fields.Float(string="Price")
    first_service = fields.Date(string="First Service")
    contract_line_id = fields.Many2one(
        "contract.line", string="Contract Line"
    )
