/*global require, module */

var idx_arr = function (arr) {
  if (arr === null) {
    return null;
  }
  return arr.map(function (val, idx) {
    return {
      idx: idx,
      val: val
    };
  });
};

var exports = {};

exports.idx_arr = idx_arr;

module.exports = exports;
