var express = require('express');
var session = require('express-session')
var app = express();

var appState = {
    guestName: undefined,
    chatting: false,
    messages: []
}

app.get('/peephole', function(req, res, next){
  if (!req.session.isOwner) res.redirect('/login');
});

app.get('/', function(req, res, next){
  if (!req.session || !req.session.isOwner) req.session = { isGuest: true, isowner: false }
  if (req.session.isOwner) res.redirect('/peephole');
  else res.redirect('/knocker')
});

app.use(session({secret:'keyboard cat'}));
module.exports = app;
