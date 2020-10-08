# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    fsm_order_id = fields.Many2one(
        'fsm.order', string='FSO'
    )
    fso_state = fields.Char(
        related="fsm_order_id.stage_name", string='FSO State'
    )
