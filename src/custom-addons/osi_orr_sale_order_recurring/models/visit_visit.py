# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


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

    def _field_create_fsm_order_prepare_values(self, sale_rec):
        self.ensure_one()
        return {
            'location_id': sale_rec.fsm_location_id.id,
            'location_directions': sale_rec.fsm_location_id.direction,
            'request_early': sale_rec.date_order,
            'scheduled_date_start': sale_rec.date_order,
            'scheduled_duration': self.hours,
            'sale_id': sale_rec.id,
            'company_id': sale_rec.company_id.id,
        }

    def _recurring_create_sale(self):
        sale_obj = self.env['sale.order']
        so_due_date = fields.Date.to_string(self.so_due_date)
        sale_rec = sale_obj.search(
            [('contract_id', '=', self.contract_id.id),
             ('date_order', '=', so_due_date)])
        sales_values = []
        if not sale_rec:
            sale_values = self.contract_id._prepare_sale(
                self.so_due_date)
            sale_values.update(
                {'contract_id': self.contract_id.id,
                 'fsm_location_id': self.contract_line_id.location_id.id})
            sale_values.setdefault('order_line', [])
            contract_line_values = self.contract_line_id._prepare_sale_line(
                sale_values=sale_values,
            )
            if contract_line_values:
                sale_values['order_line'].append(
                    (0, 0, contract_line_values)
                )
            sales_values.append(sale_values)
            sale_rec = self.env["sale.order"].create(sales_values)
            sale_rec.action_confirm()
            values = self._field_create_fsm_order_prepare_values(sale_rec)
            fsm_order = self.env['fsm.order'].create(values)
            # post message on SO
            msg_body = _(
                """Field Service Order Created: <a href=
                   # data-oe-model=fsm.order data-oe-id=%d>%s</a>
                """) % (fsm_order.id, fsm_order.name)
            sale_rec.message_post(body=msg_body)
            # post message on fsm_order
            fsm_order_msg = _(
                """This order has been created from: <a href=
                   # data-oe-model=sale.order data-oe-id=%d>%s</a>
                """) % (sale_rec.id, sale_rec.name)
            fsm_order.message_post(body=fsm_order_msg)
            self.fsm_order_id = fsm_order.id
        else:
            contract_line_values = self.contract_line_id._prepare_sale_line(
                order_id=sale_rec,
            )
            if contract_line_values:
                sale_rec.order_line = [(0, 0, contract_line_values)]
        self.sale_id = sale_rec.id
        if self.contract_id.is_po_required and not self.contract_id.po_number:
            if self.contract_line_id.sale_rep_id:
                partner_id = self.contract_line_id.sale_rep_id.partner_id
                base_url = self.env['ir.config_parameter'].sudo().get_param(
                    'web.base.url')
                partner_url = """<a href="%s/web#model=res.partner&amp;id=%s"
                class="o_mail_redirect" data-oe-id="%s"
                data-oe-model="res.partner" target="_blank">@%s</a>
                """ % (base_url, partner_id.id, partner_id.id,
                       self.contract_line_id.sale_rep_id.name)
                msg_body = """%s, <br/> PO number is missing for %s
                Contract.""" % (partner_url, self.contract_id.name)
            else:
                msg_body = """PO number is missing."""
            self.contract_id.message_post(body=msg_body)

    @api.model
    def cron_contract_recurring_create_sale(self):
        visit_rec = self.search([('sale_id', '=', False)])
        for rec in visit_rec:
            today = fields.Date.from_string(fields.Date.today())
            so_due_date = fields.Date.from_string(rec.so_due_date)
            diff_time = (so_due_date - today).days
            if (rec.contract_id.advance_number == diff_time and
                    rec.contract_id.state == 'active'):
                rec._recurring_create_sale()
            elif (so_due_date == today and
                    rec.contract_id.state == 'active'):
                rec._recurring_create_sale()
        return True
