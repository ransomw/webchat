const fs = require('fs')

const react_templates = require('react-templates')

// module-private
var require_rt_installed = false

/** allow require()ing .rt react template files */
const install_require_rt = function () {
  if (require_rt_installed) {
    return
  }
  require.extensions['.rt'] = function (module, filename) {
    var source = fs.readFileSync(filename, {encoding: 'utf8'})
    var code = react_templates.convertTemplateToReact(
            source, {
              modules: 'commonjs',
              // react minor version mismatch intended
              targetVersion: '0.14.0',
            }
        )
    module._compile(code, filename)
  }
  require_rt_installed = true
}

install_require_rt()
