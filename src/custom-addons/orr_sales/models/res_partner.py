# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class Partners(models.Model):
    _inherit = "res.partner"

    @api.depends('name')
    def name_get(self):
        res = []
        print('here')
        for record in self:
            name = record.name
            city = record.city
            state = record.state_id.name
            display_name = '%s ( %s %s )' % (name, city, state)
            res.append((record.id, display_name))
        print(res)
        return res
