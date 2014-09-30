var express = require('express');
var session = require('express-session');
var exphbs  = require('express-handlebars');
var bodyParser = require('body-parser');

var app = express();

app.use(bodyParser.urlencoded({ extended: false }));

app.use(session({
    secret:'keyboard cat'
}));

app.use(function(req, res, next) {
  if (!req.session || !req.session.isOwner) {
      req.session.isGuest = true;
      req.session.isOwner = false;
  }
  next();
});

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

app.get('/login', function(req,res,next){
    res.render('login', {
        exampleText: "example text",
        helpers: {
            foo: function(){ return 'foo'; }
	      }
    });
});

var secretKey = 'mmmsecret';

var appState = {
    guestName: null,
    chatting: false,
    messages: []
};

app.get('/keyhole', function(req, res, next){
    if (!req.session.isOwner) {
        res.render('keyhole', {});
    } else {
        res.redirect('/peephole');
    }
});

app.post('/keyhole', function(req, res, next){
    var attemptedKey = req.body.secret_key;
    if (attemptedKey === secretKey) {
        req.session.isOwner = true;
        req.session.isGuest = false;
        res.redirect('/peephole');
    } else {
        res.send("got incorrect key '" + attemptedKey + "'");
    }
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
  if (req.session.isOwner) {
      res.redirect('/peephole');
  } else {
      res.redirect('/knocker');
  }
});

module.exports = app;
