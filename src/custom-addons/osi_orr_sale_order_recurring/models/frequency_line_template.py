# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class FrequencyLineTemplate(models.Model):
    _name = "frequency.line.template"
    _description = "Frequency Line Template"

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
    so_frequency_id = fields.Many2one(
        "sale.order.frequency", string="SO Frequency"
    )
