# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class RecurrenceRecurrence(models.Model):
    _name = "recurrence.recurrence"
    _description = "Recurrence"

    name = fields.Char(string="Recurrence Name",)
    factor = fields.Integer(string="Factor",)
