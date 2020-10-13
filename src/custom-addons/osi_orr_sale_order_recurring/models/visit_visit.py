# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class VisitVisit(models.Model):
    _name = "visit.visit"
    _description = "Visit"
    _order = "so_due_date"

    contract_line_id = fields.Many2one(
        "contract.line", string="Contract Line"
    )
    contract_id = fields.Many2one(
        "contract.contract",
        related="contract_line_id.contract_id",
        string="Contract"
    )
    so_due_date = fields.Date(string="SO Due Date")
    recurrence_id = fields.Many2one(
        "recurrence.recurrence", string="Recurrence"
    )
    visit_type = fields.Selection(
        [("full", "Full"),
         ("medium", "Medium"),
         ("small", "Small")],
        string="Visit Type",
    )
    hours = fields.Float(string="Hours")
    unit_price = fields.Float(string="Price")
    # To Do Compute
    actual_hrs = fields.Float(string="Actual Hrs")
    sale_id = fields.Many2one(
        "sale.order", string="SO Number"
    )
    fsm_order_id = fields.Many2one(
        "fsm.order", string="FSO"
    )
    fso_status = fields.Char(
        related="fsm_order_id.stage_name",
        string="Status"
    )
    fso_schedule_date = fields.Date(string="FSO Schedule Date")
