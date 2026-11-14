{
    'name': 'OpenEduCat Dashboard',
    'version': '19.0.1.0',
    'license': 'LGPL-3',
    'category': 'Education',
    'summary': 'School operations dashboard for OpenEduCat',
    'author': 'OpenEduCat',
    'depends': [
        'openeducat_core',
        'openeducat_admission',
        'openeducat_attendance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/dashboard.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'openeducat_dashboard/static/src/js/dashboard.js',
            'openeducat_dashboard/static/src/xml/dashboard.xml',
            'openeducat_dashboard/static/src/scss/dashboard.scss',
        ],
    },
    'installable': True,
    'application': False,
}
