# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
import math


class ContractLine(models.Model):
    _inherit = 'contract.line'

    location_id = fields.Many2one(
        "fsm.location", string="Location"
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
        string="No. of Future Visits",
        default=13,
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
                     'first_service': self.contract_id.service_start_date,  # To do
                     }))
            if visit_setup_list:
                self.so_frequency_line_ids = False
                self.so_frequency_line_ids = visit_setup_list
        else:
            self.so_frequency_line_ids = False

    @api.multi
    def generate_visits(self):
        for rec in self:
            visits_list = []
            for freq_line in rec.so_frequency_line_ids.sorted(
                    key=lambda f_line: f_line.recurrence_id.factor,
                    reverse=True):
                floor_round_value = math.floor(
                    rec.no_future_visits / freq_line.recurrence_id.factor)
                new_due_date = False
                for no in range(1, (floor_round_value + 1)):
                    if not visits_list:
                        visits_list.append(
                            {'so_due_date': freq_line.first_service,
                             'recurrence_id': freq_line.recurrence_id.id,
                             'visit_type': freq_line.visit_type,
                             'hours': freq_line.hours,
                             'unit_price': freq_line.unit_price,
                             'contract_line_id': freq_line.contract_line_id.id
                             })
                    else:
                        if no == 1:
                            so_due_date = freq_line.first_service
                        else:
                            so_due_date = visits_list[-1].get(
                                'so_due_date') + relativedelta(
                                    months=freq_line.recurrence_id.factor)
                        exclusion_check_list = [
                            visit for visit in visits_list
                            if visit.get('so_due_date') ==
                            so_due_date and not new_due_date]
                        if exclusion_check_list:
                            new_due_date = so_due_date + relativedelta(
                                months=freq_line.recurrence_id.factor)
                            new_check_list = [
                                visit for visit in visits_list
                                if visit.get('so_due_date') ==
                                new_due_date]
                            if new_check_list:
                                new_due_date = new_due_date + relativedelta(
                                    months=freq_line.recurrence_id.factor)
                            pass
                        else:
                            if new_due_date:
                                so_due_date = new_due_date
                                new_due_date = False
                            visits_list.append(
                                {'so_due_date': so_due_date,
                                 'recurrence_id': freq_line.recurrence_id.id,
                                 'visit_type': freq_line.visit_type,
                                 'hours': freq_line.hours,
                                 'unit_price': freq_line.unit_price,
                                 'contract_line_id':
                                 freq_line.contract_line_id.id
                                 })
            if len(visits_list) >= rec.no_future_visits:
                visits_list = visits_list[0:rec.no_future_visits]
            final_visits_list = [(0, 0, visit) for visit in visits_list]
            rec.visit_ids = final_visits_list
        return True

    @api.multi
    def update_visits_pricing(self):
        for rec in self:
            # Todo
            pass
        return True
