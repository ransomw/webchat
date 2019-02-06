const nock = require('nock')

const {delay} = require('../util')
const {
  make_test,
  get_wrapper_room,
  fetch_initial_state,
  base_url,
} = require('./setup_teardown')

const HTTP_DELAY_MS = 500

const test_startup = (t) => {
  t.ok(get_wrapper_room().find(
    '.input form'
  ).exists(),
       "found text input form")
  t.ok(get_wrapper_room().find(
    '.input form input'
  ).exists(),
       "found text input element")
  t.notOk(get_wrapper_room().props().messages,
          "falsey messages prop")
  t.notOk(get_wrapper_room().props().users,
          "falsey users prop")
  t.ok(get_wrapper_room().find(
    '.chat-window .messages .loading span.loading-msg'
  ).exists(),
       "found loading message span element in chat window")
  t.ok(get_wrapper_room().find(
    '.users-list .loading span.loading-msg'
  ).exists(),
       "found loading message span element in users list")
  t.notOk(get_wrapper_room().find(
    '.chat-window .messages ul'
  ).exists(),
       "messages list absent")
  t.notOk(get_wrapper_room().find(
    '.users-list ul'
  ).exists(),
       "users list absent")
  t.end()
}

const test_http_init = (t) => {
  const nock_scope = nock(base_url)
        .get('/api/chat/users').reply(200, {
          users: [
            {
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
    t.pass("called fetch_initial_state")
    t.ok(nock_scope.isDone(),
         "called expected http mocks")
    t.ok(get_wrapper_room().props().messages,
         "truthy messages prop")
    t.ok(get_wrapper_room().props().users,
         "truthy users prop")
  })
}

const tests_main = (t) => {
  t.test("ui surface on startup",
         make_test(test_startup))
  t.test("http requests for initial state",
         make_test(test_http_init))
  t.end()
}

var exports = tests_main

module.exports = exports
