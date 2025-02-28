# -*- coding: utf-8 -*-
{
    'name': "Document Request Portal",
    'version': '17.0.1.5',
    'author': "Code OX",

    'depends': ['portal', 'project', 'sale_management', 'base', 'mail', 'sign'],

    'data': [
        'security/ir.model.access.csv',
        'views/portal_request_form_views.xml',
        'views/portal_document_request_home_and_form.xml',
        'views/portal_template_menu.xml',
        'views/portal_open_liine.xml',
        'views/menu.xml'

    ],
    'application': True,

    # 'assets': {
    #     'web.assets_frontend': [
    #         'employee_portal/static/src/scss/portal.scss',
    #         'employee_portal/static/src/css/style.css',
    #         'employee_portal/static/src/js/hr_portal.js',
    #     ],
    # },
}
