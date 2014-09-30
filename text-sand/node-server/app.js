var express = require('express');
var session = require('express-session');
var app = express();

var appState = {
    guestName: null,
    chatting: false,
    messages: []
};

app.get('/keyhole', function(req, res, next){
    if (!req.session.isOwner) {
        res.send("keyhole template unimplemented");
    } else {
        res.redirect('/peephole');
    }
});

app.post('/keyhole', function(req, res, next){
    debugger;
});

app.get('/peephole', function(req, res, next){
  if (!req.session.isOwner) {
      res.redirect('/keyhole');
  } else if (appState.guestName !== null) {
      res.send("guest at peephole, but template unimplemented");
  } else {
      res.send("peephole template unimplemented");
  }
});

app.get('/knocker', function(req, res, next){
    console.log("***********");
    console.log(req.session);
    console.log("***********");
    if (appState.guestName === null &&
        ! req.session.isGuest) {
        res.send("knocker template unimplented");
    } else if (req.session.isGuest) {
        if (appState.chatting) {
            res.redirect('/room');
        } else {
            res.send("knocker waiting template unimplemented");
        }
    } else {
        res.send("another guest is ahead of you");
    }
});

app.post('/knocker', function(req, res, next) {
    debugger;
});

app.get('/', function(req, res, next){
  if (!req.session || !req.session.isOwner) {
      req.session = { isGuest: true, isowner: false };
  }
  if (req.session.isOwner) {
      res.redirect('/peephole');
  } else {
      res.redirect('/knocker');
  }
});

app.use(session({secret:'keyboard cat'}));
module.exports = app;
