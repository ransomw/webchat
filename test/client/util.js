const path = require('path')

const path_app_src = path.join(
  __dirname, '..', '..',
  'core', 'client', 'app')

const delay = function (ms_dur) {
  return function () {
    return new Promise(function (resolve, reject) {
      setTimeout(resolve, ms_dur)
    })
  }
}

var exports = {}

exports.path_app_src = path_app_src
exports.delay = delay

module.exports = exports
