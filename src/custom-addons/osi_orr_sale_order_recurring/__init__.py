# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from . import models

from odoo import api, SUPERUSER_ID


def _deactivate_contract_cron(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref("contract.contract_cron_for_invoice").active = False
    env.ref("contract_sale_generation.contract_cron_for_sale").active = False
    env.ref("contract.contract_line_cron_for_renew").active = False
