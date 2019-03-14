/* global location */

const EventEmitter = require('events').EventEmitter

const SockJS = require('sockjs-client')

const _MSG_EVENT = 'new message'

class RoomEventEmitter extends EventEmitter {
  constructor () {
    super()
    const base_url = 'http://' + document.domain + ':' + location.port
    const sockjs_url = base_url + '/sockjs'

    /* https://github.com/sockjs/sockjs-client/issues/18 */
    window.addEventListener(
      'keydown',
      function(e) { (e.keyCode == 27 && e.preventDefault()) })

    let sock = new SockJS(sockjs_url)
    sock.onheartbeat = (ev) => {
      sock.send('backbeat')
    }
    sock.onmessage = this._on_sockjs_event.bind(this)
    sock.onclose = (ev) => {
      console.log("sockjs close event")
      console.log(ev)
    }
    this._sockjs_socket = sock
  }

  _on_sockjs_event (ev) {
    let json_data
    if (ev.data === 'connected') {
      return
    }
    try {
      json_data = JSON.parse(ev.data)
    } catch (err) {
      console.error("error parsing sockjs auction event data as JSON")
      console.error(ev)
      return
    }
    this._onData(json_data)
  }

  _onData (data) {
    if (data.msg) {
      super.emit('msg', data)
    } else if (data.action === 'join' || data.action === 'part') {
      console.log("emitting users event")
      super.emit('users', {})
    }
  }

  emit (eventName) {
    let err = new Error(
      "current implementation of event emitter " +
        "is unidirectional (server -> client)")
    err.name = 'ImplementationError'
    throw err
  }
}

module.exports = RoomEventEmitter
