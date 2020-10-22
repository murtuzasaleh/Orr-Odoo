# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    contract_id = fields.Many2one(
        "contract.contract", string="Contract"
    )

    @api.multi
    def create_contract(self):
        for rec in self:
            contract_obj = self.env['contract.contract']
            contract_vals = {
                'name': rec.origin,
                'partner_id': rec.partner_id.id,
                'contract_type': 'sale',
                'type': 'sale',
                'initial_sale_id': rec.id,
            }
            contract_line_list = []
            for line in rec.order_line:
                contract_line_list.append(
                    (0, 0, {
                        'product_id': line.product_id.id,
                        'name': line.name,
                        'quantity': line.product_uom_qty,
                        'uom_id': line.product_uom.id,
                        'price_unit': line.price_unit,
                        'discount': line.discount,
                    }))
            contract_vals.update({'contract_line_ids': contract_line_list})
            contract_obj.create(contract_vals)
        return True

    @api.multi
    def action_view_contract(self):
        action = self.env.ref('contract.action_customer_contract').read()[0]
        action['views'] = [(self.env.
                            ref('contract.contract_contract_form_view').id,
                            'form')]
        action['res_id'] = self.contract_id.id
        return action
