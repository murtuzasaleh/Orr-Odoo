# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ContractLine(models.Model):
    _inherit = 'contract.line'

    location_id = fields.Many2one(
        "res.partner", string="Location"
    )
    specific_fsm_notes = fields.Text(string="Specific FSM Notes")
    sale_rep_id = fields.Many2one(
        "res.users", string="Sales Rep"
    )
    is_subcontracted = fields.Boolean(
        string="Is Subcontracted"
    )
    tm_flat_rate = fields.Float(string="T&M or Flat rate")
    frequency_id = fields.Many2one(
        "sale.order.frequency", string="Frequency"
    )
    so_frequency_line_ids = fields.One2many(
        string="Visit Setup",
        comodel_name="sale.order.frequency.line",
        inverse_name="contract_line_id",
    )
    no_future_visits = fields.Integer(
        string="No. of Future Visits"
    )
    visit_ids = fields.One2many(
        string="Visits",
        comodel_name="visit.visit",
        inverse_name="contract_line_id",
    )

    @api.onchange('frequency_id')
    def _onchange_frequency_id(self):
        if self.frequency_id:
            visit_setup_list = []
            for freq_templ_rec in self.frequency_id.freq_template_ids:
                visit_setup_list.append((
                    0, 0,
                    {'sequence': freq_templ_rec.sequence,
                     'recurrence_id': freq_templ_rec.recurrence_id,
                     'recurrence_ids': freq_templ_rec.recurrence_ids,
                     'visit_type': freq_templ_rec.visit_type,
                     'contract_line_id': self.id,
                     }))
            self.so_frequency_line_ids = visit_setup_list
