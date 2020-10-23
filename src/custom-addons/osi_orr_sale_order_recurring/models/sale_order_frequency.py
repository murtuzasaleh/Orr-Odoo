# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrderFrequency(models.Model):
    _name = "sale.order.frequency"
    _description = "SO Frequency"

    name = fields.Char(string="Frequency Name")
    freq_template_ids = fields.One2many(
        string="Frequency Template Lines",
        comodel_name="frequency.line.template",
        inverse_name="so_frequency_id",
    )
