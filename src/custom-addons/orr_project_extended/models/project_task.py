from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        result = super().create(vals)
        if result.project_id.analytic_tag_ids:
            result.write(
                {"accounting_tag": [(6, 0, result.project_id.analytic_tag_ids.ids)]}
            )
        return result

    @api.onchange("project_id")
    def _onchange_project(self):
        result = super()._onchange_project()
        for task_id in self:
            if task_id.project_id.analytic_tag_ids:
                task_id.accounting_tag = [
                    (6, 0, task_id.project_id.analytic_tag_ids.ids)
                ]
        return result

    accounting_tag = fields.Many2many(
        "account.analytic.tag", name="Analytic Tag", readonly=True
    )

    def action_create_order(self):
        result = super().action_create_order()
        context = dict(result["context"])
        context["default_accounting_tag"] = [
            (6, 0, self.project_id.analytic_tag_ids.ids)
        ]
        result["context"] = context
        return result
