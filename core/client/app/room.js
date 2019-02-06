/*global require */

const React = require('react')
const ReactDOM = require('react-dom')

const ChatRoom = require('./components/chat_room')
const ChatRoomStore = require('./stores/chat_room_store')
const ChatRoomActions = require('./actions/chat_room_actions')
const RoomEventEmitter = require('./room_event_emitter')

const room_event_emitter = new RoomEventEmitter()

const _render = function () {
  const main_component = React.createElement(
    ChatRoom,
    ChatRoomStore.getState()
  )
  ReactDOM.render(main_component, document.getElementById('app'))
}

ChatRoomStore.listen(_render)

_render()

ChatRoomActions.fetch_initial_state()
room_event_emitter.on(
  'msg',
  (msg) => ChatRoomActions.add_msg(msg)
)
