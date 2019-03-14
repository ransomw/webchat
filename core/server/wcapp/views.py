import re

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session as login_session
from flask import jsonify

import wcapp.view_helpers as vh
from wcapp.view_helpers import ViewHelperError as VHError

from flask import Blueprint

blueprint = Blueprint(
    'views',
    __name__,
)

@blueprint.route('/')
def home():
    if 'username' not in login_session:
        return redirect(url_for('views.join'))
    return redirect(url_for('views.room'))


@blueprint.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')
    username = request.form['username']
    try:
        vh.user_join(username)
        login_session['username'] = username
    except VHError as err:
        return repr(err)
    return redirect(url_for('views.room'))


@blueprint.route('/room')
def room():
    if 'username' not in login_session:
        return redirect(url_for('views.join'))
    try:
        vh.ensure_user_joined(login_session['username'])
    except VHError as err:
        return repr(err)
    return render_template('room.html')


@blueprint.route('/api/chat/users')
def users():
    if 'username' not in login_session:
        resp = jsonify({
            'msg': "have not registered username"
        })
        resp.status_code = 401
        return resp
    try:
        return jsonify({
            'users': vh.get_users()
        })
    except VHError as err:
        resp = jsonify({
            'err': err.get_client_msg()
        })
        resp.status_code = 500
        return resp


@blueprint.route('/api/chat/messages', methods=['GET', 'POST'])
def messages():
    if 'username' not in login_session:
        resp = jsonify({
            'msg': "have not registered username"
        })
        resp.status_code = 401
        return resp
    try:
        if request.method == 'GET':
            return jsonify({
                'messages': vh.get_messages()
            })
        vh.add_message(
            login_session['username'],
            request.json['message']
        )
        return jsonify({
            'username': login_session['username'],
            'message': request.json['message']
        })
    except VHError as err:
        resp = jsonify({
            'err': err.get_client_msg()
        })
        resp.status_code = 500
        return resp

