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
      req.session.isGuest = false;
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
        res.redirect('/peephole');
    } else {
        res.send("got incorrect key '" + attemptedKey + "'");
    }
});

app.get('/peephole', function(req, res, next){
  if (!req.session.isOwner) {
      res.redirect('/keyhole');
  } else if (appState.guestName !== null) {
      res.render('peephole_wait', { guest_name: appState.guestName });
  } else {
      res.render('peephole', {});
  }
});

app.post('/peephole', function(req, res, next){
    var actionType = req.body.action_type;
    if (actionType === 'exit') {
        req.session.isOwner = false;
        res.redirect('/keyhole');
    } else if (actionType == 'open') {
        appState.chatting = true;
        res.redirect('/room');
    } else {
        throw new Error(["with owner at peephole, ",
                         "unknown action type: ",
                         actionType].join(''));
    }
});

app.get('/knocker', function(req, res, next){
    // todo xxx: check session after redirect from post
    if (appState.guestName === null &&
        ! req.session.isGuest) {
        res.render('knocker', {});
    } else if (req.session.isGuest) {
        if (appState.chatting) {
            res.redirect('/room');
        } else {
            res.render('knocker_wait', {});
        }
    } else {
        res.send("another guest is ahead of you");
    }
});

app.post('/knocker', function(req, res, next) {
    var actionType = req.body.action_type;
    if (appState.guestName !== null &&
        ! actionType) {
        res.send("you may not knock if another guest is ahead of you");
    } else if (actionType) {
        if (actionType === 'leave') {
            appState.guestName = null;
            req.session.isGuest = false;
            res.redirect('/knocker');
        } else {
            res.send("unknown action type '" + actionType + "'");
        }
    } else {
        appState.guestName = req.body.guest_name;
        req.session.isGuest = true;
        res.redirect('/knocker');
    }
});

app.get('/', function(req, res, next){
  if (req.session.isOwner) {
      res.redirect('/peephole');
  } else {
      res.redirect('/knocker');
  }
});

module.exports = app;
