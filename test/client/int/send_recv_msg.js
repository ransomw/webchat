const nock = require('nock')

const {delay} = require('../util')
const {
  make_test,
  get_wrapper_room,
  fetch_initial_state,
  base_url,
  sim_recv_msg,
} = require('./setup_teardown')

const HTTP_DELAY_MS = 500
const PROMISE_DELAY_MS = 50

const test_send_msg = (t) => {
  nock(base_url)
    .get('/api/chat/users').reply(200, {
      users: [
        {
          username: 'alice',
          username: 'bob',
        },
      ]})
    .get('/api/chat/messages').reply(200, {
      messages: []})
  const nock_scope_send = nock(base_url)
        .post('/api/chat/messages', {
          message: 'hello',
        }).reply(200, {})
  return Promise.resolve().then(() => {
    fetch_initial_state()
  }).then(delay(HTTP_DELAY_MS)).then(() => {
    get_wrapper_room().find(
      '.input form input'
    ).first().simulate('change', {target: {value: 'hello'}})
    t.equal(get_wrapper_room().state('str_msg'), 'hello',
            "found expected message in component state")
    get_wrapper_room().find(
      '.input form'
    ).first().simulate('submit')
  }).then(delay(HTTP_DELAY_MS)).then(() => {
    t.pass("simulated message form submit")
    t.ok(nock_scope_send.isDone(),
         "called expected http mocks with expected POST data")
  })
}

const test_recv_msg = (t) => {
  nock(base_url)
    .get('/api/chat/users').reply(200, {
      users: [
        {
          username: 'alice',
          username: 'bob',
        },
      ]})
    .get('/api/chat/messages').reply(200, {
      messages: [
        {
          username: 'bob',
          msg: 'hello',
        },
      ]})
  return Promise.resolve().then(() => {
    fetch_initial_state()
  }).then(delay(HTTP_DELAY_MS)).then(() => {
    t.equal(get_wrapper_room().props().messages.length, 1,
            "one message upon init")
    sim_recv_msg({
      username: 'alice',
      msg: 'hi',
    })
  }).then(delay(PROMISE_DELAY_MS)).then(() => {
    t.equal(get_wrapper_room().props().messages.length, 2,
            "two messages after simulated receive")
  })
}

const tests_main = (t) => {
  t.test("test sending a message",
         make_test(test_send_msg))
  t.test("test receiving a message",
         make_test(test_recv_msg))
  t.end()
}

var exports = tests_main

module.exports = exports
