# Copyright (C) Camptocamp Austria (<http://www.camptocamp.at>)
# Copyright 2018 Open Source Integrators (http://www.opensourceintegrators.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    is_discount = fields.Boolean(
        string='Early Payment Discount',
        help="Check this box if this payment term has a discount. "
             "If discount is used the remaining amount of the invoice "
             "will not be paid"
    )
    is_exclude_shipping_lines = fields.Boolean(
        string='Exclude Shippling Lines Discount',
        help="Check this box if want to exclude shipping charges from discount"
    )
    is_exclude_taxes_discount = fields.Boolean(
        string='Exclude Taxes Discount',
        help="Check this box if want to exclude taxes from discount"
    )

    def _get_payment_term_discount(self, invoice=None, payment_date=None,
                                   amount=0.0):
        payment_discount = 0.0
        discount_account_id = 0.0
        for payment_term in self:
            for line in payment_term.line_ids:
                # Check payment date discount validation
                invoice_date = fields.Date.from_string(
                                      invoice.date_invoice)
                till_discount_date = invoice_date + relativedelta(
                    days=line.discount_days)
                if line.discount and payment_date <= till_discount_date:
                    payment_discount = round((amount * line.discount) / 100.0,
                                             2)
                    if invoice.type in ('out_invoice','in_refund'):
                        discount_account_id = line.discount_expense_account_id.id
                    else:
                        discount_account_id = line.discount_income_account_id.id
                    break
        return payment_discount, discount_account_id, amount

    @api.multi
    def _check_payment_term_discount(self, invoice=None, payment_date=None):
        payment_discount = 0.0
        applied_amount_total = 0.0
        discount_account_id = 0.0
        if not invoice:
            return payment_discount, discount_account_id, applied_amount_total
        if not payment_date:
            payment_date = fields.Date.context_today(self)
        else:
            payment_date = fields.Date.from_string(payment_date)
        for payment_term in self.filtered(lambda p: p.is_discount):
            if payment_term.is_exclude_taxes_discount:
                amount = invoice.amount_untaxed_invoice_signed
            else:
                amount = invoice.amount_total
            if payment_term.is_exclude_shipping_lines:
                amount -= invoice.shipping_lines_total
            discount_information = payment_term._get_payment_term_discount(
                invoice, payment_date, amount)
            payment_discount = discount_information[0]
            discount_account_id = discount_information[1]
            applied_amount_total = invoice.residual
        return payment_discount, discount_account_id, applied_amount_total


class AccountPaymentTermLine(models.Model):
    _inherit = 'account.payment.term.line'

    is_discount = fields.Boolean(related='payment_id.is_discount',
                                 string='Early Payment Discount', readonly=True)
    discount = fields.Float('Discount (%)', digits=(4,2))
    discount_days = fields.Integer('Discount Days')
    discount_income_account_id = fields.Many2one(
        'account.account',
        string='Discount Income Account',
        view_load=True,
        help="This account will be used to post the discount income"
    )
    discount_expense_account_id = fields.Many2one(
        'account.account',
        string='Discount Expense Account',
        view_load=True,
        help="This account will be used to post the discount expense"
    )

    @api.onchange('discount')
    def OnchangeDiscount(self):
        if not self.discount: return {}
        self.value_amount = round(1-(self.discount/100.0),2)
