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
        return True
