require.config({
    baseUrl: 'assets',
    paths: {
        'jquery': 'bower_components/jquery/dist/jquery',
        'lodash': 'bower_components/lodash/dist/lodash'
    }
});


require([
    'jquery',
    'lodash'
], function ($, _) {
    "use strict";

    console.log("top of main");
});
