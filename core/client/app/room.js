/*global require */

var io = require('socket.io-client');
var _ = require('lodash');

var React = require('react');
var ReactDOM = require('react-dom');

var ChatRoom = require('./components/chat_room');

var ChatRoomStore = require('./stores/chat_room_store');
var chat_room_actions = require('./actions/chat_room_actions');
var RoomEventEmitter = require('./room_event_emitter');

var room_event_emitter = new RoomEventEmitter();

var _render = function () {
  var main_component = React.createElement(
    ChatRoom,
    ChatRoomStore.getState()
  );
  ReactDOM.render(main_component, document.getElementById('app'));
};

ChatRoomStore.listen(_render);

_render();

chat_room_actions.fetch_initial_state();
room_event_emitter.on(
  'msg',
  (msg) => chat_room_actions.add_msg(msg)
);
