from odoo import api, fields, models

class FSMOrder(models.Model):
    _inherit = 'fsm.order'

    accounting_tag = fields.Many2many(
        'account.analytic.tag',readonly=True
        
    )