# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def default_get(self, fields):
        res = super(IrAttachment, self).default_get(fields)
        # check for active id
        active_id = self._context.get("active_id")
        if self.env.context.get("active_model") == "project.project" and active_id:
            # get active project
            active_project = self.env["project.project"].browse(active_id)
            # get active customer
            active_customer = active_project.partner_id
            # assign partner_id in return dictionary
            res["partner_id"] = active_customer.id
        return res
