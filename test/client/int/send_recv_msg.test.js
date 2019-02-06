const tape = require('blue-tape')

tape.test("send and receive messages",
          require('./send_recv_msg'))
