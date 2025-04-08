{
    'name':'Invoice Analysis Excel',
    'version':'17.0.1.0',
    'summary':'',
    'website':'',
    'depends':['base','sale_management', 'report_xlsx', 'account', 'web'],
    'data':[
    ],
    'assets': {
        'web.assets_backend': [
            'invoice_analysis_excel/static/src/js/pivot_download_button.js',
            'invoice_analysis_excel/static/src/js/pivot_buttons_template_inherit.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}