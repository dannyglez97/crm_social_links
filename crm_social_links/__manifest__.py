{
    'name': "CRM Social Links",
    'summary': "Agrega campos para redes sociales a los contactos",
    'description': """
        Extiende el módulo CRM para agregar campos de redes sociales
        (Facebook, LinkedIn, Twitter) a los contactos.
    """,
    'author': "DANNY",
    'website': "https://www.tuempresa.com",
    'category': 'CRM',
    'version': '16.0.1.0.0',
    'depends': ['website','base', 'crm'],
    'data': [
        'security/ir.model.access.csv',               
        'views/res_partner_views.xml',
        'views/template.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            'crm_social_links/static/src/css/style.css',
            'crm_social_links/static/src/js/script.js',
        ],
    },
    'installable': True,
    'application': False,
}