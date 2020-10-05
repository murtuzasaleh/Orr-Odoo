from odoo import fields, models


class FSMOrder(models.Model):
    _inherit = 'fsm.order'

    private_notes = fields.Text(string='Private Notes')
    public_notes = fields.Text(string='Public Notes')

    previous_private_notes = fields.Text(string='Previous Private Notes',compute='_get_last_three_private_notes')
    previous_public_notes = fields.Text(string='Previous Public Notes',compute='_get_last_three_public_notes')

    def _clear_html(self,value):
        new_str = value
        new_str = new_str.replace('<p>','')
        new_str = new_str.replace('</p>','')
        return new_str
    
    def _get_last_three_private_notes(self):
        orders = self.env['fsm.order'].search([('equipment_id','=',self.equipment_id.id),('id','!=',self.id)] ,order='date_end desc',limit=3)
        private_note = ''
        public_note = ''
        print(len(orders))
        for order in orders:
            if order:
                if order.private_notes:
                    if(len(private_note) > 0):
                        private_note = private_note.join('\n')
                    private_note = private_note.join(order.private_notes)

                if order.public_notes:
                    if(len(public_note) > 0):
                        public_note = public_note.join('\n')
                    public_note = public_note.join(order.public_notes)
                   ## print(public_note)
        if len(private_note) == 0:
            private_note = 'no history'
        self.previous_private_notes = self._clear_html(private_note)
        if len(public_note) == 0:
            public_note = 'no history'
        self.previous_public_notes = self._clear_html(public_note)




    def _get_last_three_public_notes(self):
        pass

   
