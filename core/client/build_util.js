/*global require, module, __dirname */

var fs = require('fs');

var read_file = function (file_path) {
  return new Promise(function (resolve, reject) {
    fs.readFile(file_path, 'utf8', function (err, data) {
      if (err) {
        reject(err);
      } else {
        resolve(data);
      }
    });
  });
};

var write_file = function (file_path, file_str) {
  return new Promise(function (resolve, reject) {
    fs.writeFile(file_path, file_str, function (err) {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
};

var exports = {};

exports.read_file = read_file;
exports.write_file = write_file;

module.exports = exports;
