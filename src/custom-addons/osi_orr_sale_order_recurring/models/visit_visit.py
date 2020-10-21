# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


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

    def _recurring_create_sale(self):
        sale = self.contract_id.recurring_create_sale()
        self.sale_id = sale.id
        return True

    @api.model
    def cron_contract_recurring_create_sale(self):
        visit_rec = self.search([('sale_id', '=', False)])
        for rec in visit_rec:
            today = fields.Date.from_string(fields.Date.today())
            so_due_date = fields.Date.from_string(rec.so_due_date)
            diff_time = (so_due_date - today).days
            if rec.contract_id.advance_number == diff_time:
                rec._recurring_create_sale()
            elif so_due_date == today:
                rec._recurring_create_sale()
        return True
