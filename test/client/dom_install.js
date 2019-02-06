const jsdom = require('jsdom')

var dom_impl_installed = false

const install_dom_impl = function () {
  if (dom_impl_installed) {
    return
  }

  const doc = jsdom.jsdom([
    '<!doctype html>',
    '<html>',
    '<body>',
    '<div id="app"></div>',
    '</body>',
    '</html>',
  ].join(''))
  const win = doc.defaultView
  // const $ = jquery(win)

  global.document = doc
  global.window = win
  // global.$ = $
  // additional browser-like globals for react
  global.navigator = win.navigator

  dom_impl_installed = true
}

install_dom_impl()
