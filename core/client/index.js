/*global require, module */

var path = require('path');
var fs = require('fs');

const fse = require('fs-extra');

var build_js = require('./build_steps').build_js;
var build_styles = require('./build_steps').build_styles;

var build_client = function (dir_client, opt_args) {
  fse.ensureDirSync(dir_client);
  return Promise.all([
    build_js(path.join(dir_client, 'js'), opt_args),
    build_styles(path.join(dir_client, 'styles'), opt_args)
  ]);
};

var exports = {};

exports.build_client = build_client;

module.exports = exports;
