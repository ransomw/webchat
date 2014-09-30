var express = require('express');
var session = require('express-session');
exphbs  = require('express-handlebars');
var app = express();

app.use(session({
    secret:'keyboard cat'
}));

app.use(function(req, res, next) {
  if (!req.session || !req.session.isOwner) {
      req.session.isGuest = true;
      req.session.isowner = false;
  }
  console.log('SESSION', req.session)
  next();
})

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

app.get('/login', function(req,res,next){
    res.render('login', {
        exampleText: "example text"
    })
});

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
  console.log('SESSION', req.session)
  if (req.session.isOwner) {
      res.redirect('/peephole');
  } else {
      res.redirect('/knocker');
  }
});

module.exports = app;
