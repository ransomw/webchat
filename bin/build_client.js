/*global require, __dirname */

var path = require('path');

const build_client = require('../core/client').build_client;

const argv = require('yargs').options({
  'p': {
    alias: 'dir_out',
    desc: "output directory path",
    type: 'string',
    default: path.join(
      __dirname, '..', 'build', 'server_static', 'client')
  },
  'c': {
    alias: 'cts',
    desc: "continuous client build",
    type: 'boolean'
  }
}).argv;

Promise.resolve().then(function () {
  return build_client(argv.dir_out, {cts: argv.cts});
}).then(function () {
  console.log("client build finished");
}, function (err) {
  console.error("client build failed");
  console.error(err);
});
