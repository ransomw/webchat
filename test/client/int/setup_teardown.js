const React = require('react')
const proxyquire = require('proxyquire').noPreserveCache()
const {
  mount: mount,
  configure: configure_enzyme,
} = require('enzyme')
const Adapter = require('enzyme-adapter-react-16')

configure_enzyme({ adapter: new Adapter() })

const {path_app_src} = require('../util')

const base_url = 'http://www.example.com'

const sources = proxyquire(
  path_app_src + '/sources',
  {
    '../base_url': base_url + '/',
  }
)
const alt = proxyquire(
  path_app_src + '/alt',
  {}
)
const ChatRoomActions = proxyquire(
  path_app_src + '/actions/chat_room_actions',
  {
    '../sources': sources,
  }
)
const ChatRoomStore = proxyquire(
  path_app_src + '/stores/chat_room_store',
  {
    '../sources': sources,
    '../actions/chat_room_actions': ChatRoomActions,
  }
)
const ChatRoom = proxyquire(
  path_app_src + '/components/chat_room',
  {
    '../actions/chat_room_actions': ChatRoomActions,
  }
)

const fetch_initial_state = () => ChatRoomActions.fetch_initial_state()
const sim_recv_msg = (msg_data) => ChatRoomActions.add_msg(msg_data)

// per-test variables
let wrapper_room

const render_room = function () {
  const main_component = React.createElement(
    ChatRoom,
    ChatRoomStore.getState()
  )
  wrapper_room = mount(main_component)
}

const get_wrapper_room = () => wrapper_room

const setup = function (t) {
  render_room()
  ChatRoomStore.listen(render_room)
  t.end()
}

const teardown = function (t) {
  ChatRoomStore.unlisten(render_room)
  alt.recycle()
  get_wrapper_room().unmount()
  t.end()
}

const make_test = function (test_fn) {
  return function (t) {
    t.test("setup", setup)
    t.test("run test", test_fn)
    t.test("teardown", teardown)
    t.end()
  }
}

var exports = {}

exports.make_test = make_test
exports.get_wrapper_room = get_wrapper_room
exports.fetch_initial_state = fetch_initial_state
exports.base_url = base_url
exports.sim_recv_msg = sim_recv_msg

module.exports = exports
