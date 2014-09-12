define([
    'config/server'
], function (serv_config) {


    var _SERVER_URL = 'http://' +
            [serv_config.server_domain, serv_config.server_port].join(':'),
				_PHOTO_URL = [_SERVER_URL,
                      'assets/img/linkedin_profile.jpg'].join('/');
    return {
        photo_url: _PHOTO_URL
    };

});
