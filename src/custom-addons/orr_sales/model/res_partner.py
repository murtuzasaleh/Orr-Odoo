from odoo import api, fields, models


class Partners(models.Model):
    _inherit = "res.partner"

    @api.depends('name')
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            city = record.city
            state = record.state_id.name
            display_name = '%s ( %s %s )' % (name,city,state)
            res.append((record.id,display_name))
        print(res)
        return res

    

