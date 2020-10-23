# -*- coding: utf-8 -*-
from collections import OrderedDict

from odoo import http, _
from odoo.http import request
from odoo import fields
from odoo.addons.portal.controllers.portal import (
    get_records_pager,
    CustomerPortal,
    pager as portal_pager,
)

from odoo.osv.expression import OR

from odoo.exceptions import AccessError, MissingError


class CustomerPortal(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        Project = request.env["project.project"]
        Task = request.env["project.task"]

        projects = Project.sudo().search([("user_id", "=", request._uid)])
        domain = [
            "|",
            ("project_id", "in", projects.ids),
            ("user_id", "=", request._uid),
        ]
        values["job_order_count"] = Task.search_count(domain)
        print("::::::::::::::values", values)
        return values

    @http.route(
        ["/user/job_orders", "/user/job_orders/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_user_job_orders(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw
    ):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Title"), "order": "name"},
            "stage": {"label": _("Stage"), "order": "stage_id"},
            "update": {
                "label": _("Last Stage Update"),
                "order": "date_last_stage_update desc",
            },
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {
            "content": {
                "input": "content",
                "label": _('Search <span class="nolabel"> (in Content)</span>'),
            },
            "message": {"input": "message", "label": _("Search in Messages")},
            "customer": {"input": "customer", "label": _("Search in Customer")},
            "stage": {"input": "stage", "label": _("Search in Stages")},
            "all": {"input": "all", "label": _("Search in All")},
        }
        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        projects = (
            request.env["project.project"]
            .sudo()
            .search([("user_id", "=", request._uid)])
        )
        domain = [
            "|",
            ("project_id", "in", projects.ids),
            ("user_id", "=", request._uid),
        ]
        for proj in projects:
            searchbar_filters.update(
                {
                    str(proj.id): {
                        "label": proj.name,
                        "domain": [("project_id", "=", proj.id)],
                    }
                }
            )

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain += searchbar_filters[filterby]["domain"]

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups("project.task", domain)
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ("content", "all"):
                search_domain = OR(
                    [
                        search_domain,
                        [
                            "|",
                            ("name", "ilike", search),
                            ("description", "ilike", search),
                        ],
                    ]
                )
            if search_in in ("customer", "all"):
                search_domain = OR([search_domain, [("partner_id", "ilike", search)]])
            if search_in in ("message", "all"):
                search_domain = OR(
                    [search_domain, [("message_ids.body", "ilike", search)]]
                )
            if search_in in ("stage", "all"):
                search_domain = OR([search_domain, [("stage_id", "ilike", search)]])
            domain += search_domain

        # task count
        task_count = request.env["project.task"].sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/job_orders",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
            },
            total=task_count,
            page=page,
            step=self._items_per_page,
        )
        # content according to pager and archive selected
        tasks = (
            request.env["project.task"]
            .sudo()
            .search(
                domain, order=order, limit=self._items_per_page, offset=pager["offset"]
            )
        )
        grouped_tasks = [tasks]
        request.session["my_tasks_history"] = tasks.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "projects": projects,
                "tasks": tasks,
                "page_name": "job_order",
                "archive_groups": archive_groups,
                "default_url": "/my/job_orders",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "sortby": sortby,
                "searchbar_filters": OrderedDict(sorted(searchbar_filters.items())),
                "filterby": filterby,
                "is_job_order": True,
                "grouped_tasks": grouped_tasks,
            }
        )
        return request.render("project.portal_my_tasks", values)

    @http.route(["/my/job_order/<int:task_id>"], type="http", auth="user", website=True)
    def portal_user_job_order(self, task_id=None, access_token=None, **kw):
        task = request.env["project.task"].sudo().browse(task_id)
        try:
            task_sudo = self._document_check_access(
                "project.task", task_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        vals = {
            "task": task,
            "user": request.env.user,
            "page_name": "job_order",
            "is_job_order": True,
        }
        history = request.session.get("my_tasks_history", [])
        vals.update(get_records_pager(history, task))
        return request.render("project.portal_my_task", vals)
