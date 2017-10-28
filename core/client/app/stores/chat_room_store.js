/*global require, module */

var _ = require('lodash');
var nets = require('nets');

var alt = require('../alt');

var chat_room_actions = require('../actions/chat_room_actions');

var _chat_fetch = function (endpoint) {
  return new Promise(function (resolve, reject) {
    nets({
      url: 'api/chat/' + endpoint,
      jar: true,
      json: true,
      encoding: undefined
    }, function(err, resp, body) {
      if (err) {
        reject(err);
      } else {
        resolve(body);
      }
    });
  });
};

var ChatRoomStore = alt.createStore({
  displayName: 'ChatRoomStore',

  bindListeners: {
    fetch_messages_all: chat_room_actions.fetch_messages_all,
    send_message: chat_room_actions.send_message,
    init_state: chat_room_actions.fetch_initial_state,
    add_msg: chat_room_actions.add_msg,
  },

  state: {
    users: null,
    messages: null
  },

  publicMethods: {
    test_method: function () {
      console.log("test_method");
    }
  },

  init_state: function () {
    console.log("store init_state");
    return Promise.all([
      this.fetch_users(),
      this.fetch_messages_all()
    ]);
  },

  fetch_users: function () {
    var self = this;
    return _chat_fetch('users').then(function (res_users) {
      if (!res_users.users) {
        alert("error fetching users see console for details");
        console.log("error fetching users");
        console.log(res_users);
      } else {
        self.setState({users: res_users.users});
      }
    });
  },

  fetch_messages_all: function () {
    var self = this;
    return _chat_fetch('messages').then(function (res_messages) {
      if (!res_messages.messages) {
        alert("error fetching messages. see console for details");
        console.log("error fetching messages");
        console.log(res_messages);
      } else {
        self.setState({messages: res_messages.messages});
      }
    });
  },

  send_message: function (promise_send) {
    console.log("state send_message: promise_send");
    console.log(promise_send);
  },

  add_msg: function (str_msg) {
    var messages = this.state.messages;
    this.setState({messages: _.concat(messages, str_msg)});
  }
});

var exports = ChatRoomStore;
module.exports = exports;
