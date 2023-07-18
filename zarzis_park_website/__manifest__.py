# -*- coding: utf-8 -*-
{
    'name': "Website zarzis park",
    'version': '16.0',
    'author': "SOFTIFI",
    'category': "Website",
    'summary': "Website zarzis park",
    'data': [
        'views/my_footer.xml',
        'views/custom_homepage_url.xml',
        'views/pages/update_request_template.xml',
        'views/pages/check_template.xml',
        'views/pages/request_template.xml',
        'views/pages/rental_template.xml',
        'views/pages/local_details_template.xml',
        'views/pages/list_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # css
            'zarzis_park_website/static/src/js/dist/sweetalert2.min.css',
            'zarzis_park_website/static/src/css/owl.carousel/owl.carousel.min.css',
            'zarzis_park_website/static/src/css/owl.carousel/owl.theme.default.min.css',
            'zarzis_park_website/static/src/css/swiper/swiper.css',
            'zarzis_park_website/static/src/css/footer.css',
            'zarzis_park_website/static/src/css/list.css',
            'zarzis_park_website/static/src/css/details.css',
            'zarzis_park_website/static/src/css/add.css',
            'zarzis_park_website/static/src/css/search_list.css',
            'zarzis_park_website/static/src/css/style.css',
            'zarzis_park_website/static/src/css/update.css',
            'zarzis_park_website/static/src/css/rental.css',
            'zarzis_park_website/static/src/css/request.css',
            # js
            'zarzis_park_website/static/src/js/dist/sweetalert2.all.min.js',
            'zarzis_park_website/static/src/js/owl.carousel/owl.carousel.min.js',
            'zarzis_park_website/static/src/js/swiper/swiper.js',
            'zarzis_park_website/static/src/js/details.js',
            'zarzis_park_website/static/src/js/list.js',
            'zarzis_park_website/static/src/js/check.js',
            'zarzis_park_website/static/src/js/update.js',
            'zarzis_park_website/static/src/js/rental.js',
        ],
    },
    'demo': [],
    'depends': ['zarzis_park_erp', 'website', 'portal'],
    'installable': True,
}


