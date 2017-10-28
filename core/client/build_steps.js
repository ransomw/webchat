/*global require, module, __dirname  */

var path = require('path');
var fs = require('fs');

const fse = require('fs-extra');
const browserify = require('browserify');
const watchify = require('watchify');
const react_templatify = require('react-templatify');
const less = require('less');

const read_file = require('./build_util').read_file;
const write_file = require('./build_util').write_file;

var updated_react_templatify = function (file, options) {
  var opts = options || {};
  opts.targetVersion= '0.14.0';
  return react_templatify(file, opts);
};

const do_build_step = function (fn_do_once, path_watch, cts) {
  return fn_do_once().then(function () {
    if (cts) {
      fs.watch(path_watch, {recursive: true}, () => {
        fn_do_once()
          .catch(function (err) {
            console.log("client build error");
            console.log(err);
          });
      });
    }
  });
};

const build_js_file = function (path_src, path_out, opt_args) {
  const opts = opt_args || {};
  const make_write_bundle = function (bfy, path_bundle) {
    return function () {
      return new Promise(function (resolve, reject) {
        var stream_bundle = bfy.bundle();
        stream_bundle.pipe(fs.createWriteStream(path_bundle));
        stream_bundle.on('end', function () {
          resolve();
        });
      });
    };
  };
  const arr_plugins = [];
  if (opts.cts) {
    arr_plugins.push(watchify);
  }
  const arr_transforms = [];
  arr_transforms.push(updated_react_templatify);
  const bfy = browserify({
    entries: [path_src],
    cache: {},
    packageCache: {},
    debug: true, // source maps
    plugin: arr_plugins,
    transform: arr_transforms
  });
  var write_bundle = make_write_bundle(bfy, path_out);
  if (opts.cts) {
    bfy.on('update', write_bundle);
  }
  return write_bundle();
};


const build_style = function (path_src_file, path_output, opt_args) {
	const opts = opt_args || {};
  const dir_src = path.dirname(path_src_file);
	const do_once = function () {
    return read_file(path_src_file)
      .then(function (str_less_input) {
        return less.render(str_less_input, {
          paths: [
            dir_src,
            path.join(dir_src, 'vendor') // slightly janky boilerplate
          ]
        });
      }).then(function (less_output) {
        var str_css = less_output.css;
        var str_sourcemap = less_output.sourcemap;
        var arr_imports = less_output.imports;
        return write_file(path_output, str_css);
      });
	};
  return do_build_step(do_once, dir_src, opts.cts);
};

const build_js = function (dir_out, opt_args) {
  // clean before every build
  if (fs.existsSync(dir_out)) {
    fse.removeSync(dir_out);
  }
  fse.ensureDirSync(dir_out);
  return Promise.all([
    build_js_file(
      path.join(__dirname, 'app', 'room.js'),
      path.join(dir_out, 'room.js'),
      opt_args
    )
  ]);
};

const build_styles = function (dir_out, opt_args) {
  // clean before every build
  if (fs.existsSync(dir_out)) {
    fse.removeSync(dir_out);
  }
  fse.ensureDirSync(dir_out);
  return Promise.all([
    build_style(
      path.join(__dirname, 'styles', 'room.less'),
      path.join(dir_out, 'room.css'),
      opt_args
    ),
    build_style(
      path.join(__dirname, 'styles', 'join.less'),
      path.join(dir_out, 'join.css'),
      opt_args
    )
  ]);
};

var exports = {};

exports.build_js = build_js;
exports.build_styles = build_styles;

module.exports = exports;
