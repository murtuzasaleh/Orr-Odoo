# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BankPaymentLine(models.Model):
    _inherit = "bank.payment.line"

    discount_amount = fields.Monetary(
        compute="_compute_discount_amount", currency_field="currency_id"
    )
    total_amount = fields.Monetary(
        compute="_compute_total_amount", currency_field="currency_id"
    )

    @api.depends("amount_currency", "discount_amount")
    def _compute_total_amount(self):
        for line in self:
            line.total_amount = line.amount_currency + line.discount_amount

    @api.multi
    @api.depends("payment_line_ids", "payment_line_ids.discount_amount")
    def _compute_discount_amount(self):
        for bline in self:
            discount_amount = sum(bline.mapped("payment_line_ids.discount_amount"))
            bline.discount_amount = discount_amount

    def reconcile(self):
        self.ensure_one()
        amlo = self.env["account.move.line"]
        transit_mlines = amlo.search([("bank_payment_line_id", "=", self.id)])
        for line in transit_mlines:
            ap_mlines = line.invoice_id.move_id.line_ids.filtered(
                lambda x: x.account_id == line.account_id
            )
            lines_to_rec = line
            lines_to_rec += ap_mlines
            lines_to_rec.reconcile()
