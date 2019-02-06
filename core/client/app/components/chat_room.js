const Component = require('react').Component

const rt_chat_room = require('../templates/chat_room.rt')

const actions = require('../actions/chat_room_actions')
const bind_handlers = require('./util/bind_handlers')

class ChatRoom extends Component {
  constructor(props) {
    super(props)
    bind_handlers(this, /^handle_/)
    this.state = {
      str_msg: '',
    }
  }

  handle_change_str_msg(ev) {
    this.setState({str_msg: ev.target.value})
  }

  handle_submit_msg(ev) {
    actions.send_message(this.state.str_msg)
    this.setState({str_msg: ''})
  }

  render() {
    return rt_chat_room.call(this)
  }
}

var exports = ChatRoom
module.exports = exports
