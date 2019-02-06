/*global require, module, location */

const alt = require('../alt')

const _chat_send = require('../sources').chat_send

const chat_room_actions = alt.createActions({
  send_message: function (str_msg) {
    return function (dispatch) {
      dispatch() // triggers action in store
      _chat_send('messages', {message: str_msg})
        .catch(function (err) {
          alert("send message error, see console for details")
          console.log(err)
        })
    }
  },

  add_msg: function (str_msg) {
    return str_msg
  },

  // documented patterns fetches in actions.. for the
  // sake of sandboxing, they're currently in data store
  fetch_initial_state: function () {
    return function (dispatch) {
      dispatch()
    }
  },

  fetch_messages_all: function () {
    return function (dispatch) {
      console.log("actions fetch_messages_all")
      dispatch()
    }
  }
})

var exports = chat_room_actions

module.exports = exports
