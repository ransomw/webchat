/* global location */

const io = require('socket.io-client')
const EventEmitter = require('events').EventEmitter

const _MSG_EVENT = 'new message'

class RoomEventEmitter extends EventEmitter {
  constructor () {
    super()
    let socket = io.connect('http://' + document.domain + ':' +
                            location.port)

    socket.on('connect', function () {
      console.log("websocket conn established");
    });

    socket.on(_MSG_EVENT,
              (data) => this._onMsg(data))
    this._socketioSocket = socket
  }

  _onMsg (data) {
    super.emit('msg', data)
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
