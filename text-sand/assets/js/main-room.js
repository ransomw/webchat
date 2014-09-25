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

    var $messages = $('#messages');

    var update_msgs = function () {
        $.get('room/api').then(function (messages) {
            $messages.html(messages.replace(/\n/g, '<br/>'));
        });
    };

    window.setInterval(function () {
        update_msgs();
    }, 1000); // ms


    $('#new-message').on('keypress', function(event) {
        // ENTER & non-empty.
        if (event.keyCode === 13 && event.target.value.length) {
            $.post('room/api', {'message': event.target.value});
            event.target.value = '';
        }
    });

});
