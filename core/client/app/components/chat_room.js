/*global require, module */

var React = require('react');

var rt_chat_room = require('../templates/chat_room.rt');

var actions = require('../actions/chat_room_actions');

var ChatRoom = React.createClass({
  getInitialState: function() {
    return {str_msg: ''};
  },

  handle_change_str_msg: function(ev) {
    this.setState({str_msg: ev.target.value});
  },

  handle_submit_msg: function (ev) {
    actions.send_message(this.state.str_msg);
    this.setState({str_msg: ''});
  },

  render: rt_chat_room
});

var exports = ChatRoom;
module.exports = exports;
