/*global require, module, location */

var nets = require('nets');

var alt = require('../alt');


var _chat_send = function (endpoint, data) {
  return new Promise(function (resolve, reject) {
    nets({
      url: 'api/chat/' + endpoint,
      method: 'POST',
      jar: true,
      json: data,
      encoding: undefined
    }, function(err, resp, body) {
      if (err) {
        reject(err);
      } else if (resp.statusCode !== 200) {
        reject({
          status_code: resp.statusCode,
          body: body
        });
      } else {
        resolve(body);
      }
    });
  });
};

var chat_room_actions = alt.createActions({
  send_message: function (str_msg) {
    return function (dispatch) {
      console.log("actions send_message: str_msg");
      console.log(str_msg);
      dispatch(); // triggers action in store
      _chat_send('messages', {message: str_msg})
        .catch(function (err) {
          alert("send message error, see console for details");
          console.log(err);
        });
    };
  },

  add_msg: function (str_msg) {
    return str_msg;
  },

  // documented patterns fetches in actions.. for the
  // sake of sandboxing, they're currently in data store
  fetch_initial_state: function () {
    return function (dispatch) {
      console.log("actions fetch_initial_state");
      dispatch();
    };
  },

  fetch_messages_all: function () {
    return function (dispatch) {
      console.log("actions fetch_messages_all");
      dispatch();
    };
  }
});

var exports = chat_room_actions;

module.exports = exports;
