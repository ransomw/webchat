const nets = require('nets')

const base_url = require('../base_url')

const chat_fetch = (endpoint) => {
  return new Promise((resolve, reject) => {
    nets({
      url: base_url + 'api/chat/' + endpoint,
      jar: true,
      json: true,
      encoding: undefined
    }, (err, resp, body) => {
      if (err) {

        console.error("_chat_fetch error")
        console.error(err)

        reject(err)
      } else {
        resolve(body)
      }
    })
  })
}


const chat_send = (endpoint, data) => {
  return new Promise((resolve, reject) => {
    nets({
      url: base_url + 'api/chat/' + endpoint,
      method: 'POST',
      jar: true,
      json: data,
      encoding: undefined
    }, (err, resp, body) => {
      if (err) {
        reject(err)
      } else if (resp.statusCode !== 200) {
        reject({
          status_code: resp.statusCode,
          body: body
        })
      } else {
        resolve(body)
      }
    })
  })
}


var exports = {}

exports.chat_fetch = chat_fetch
exports.chat_send = chat_send

module.exports = exports
