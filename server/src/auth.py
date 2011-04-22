#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4; indent-tabs-mode: nil; coding: utf-8; -*-
# vim:set ft=python ts=4 sw=4 sts=4 autoindent:

'''
Authentication mechanisms.

Author:     Pontus Stenetorp    <pontus is s u-tokyo ac jp>
Version:    2011-04-21
'''

from hashlib import sha512

from common import ProtocolError
from config import USER_PASSWORD
from message import display_message
from session import get_session


# To raise if the authority to carry out an operation is lacking
class NotAuthorisedError(ProtocolError):
    def __init__(self, attempted_action):
        self.attempted_action = attempted_action

    def json(self, json_dic):
        json_dic['exception'] = 'notAuthorised'
        # TODO: Really send this message?
        display_message('Login required to perform "%s"'
                % self.attempted_action, 'error', 5)
        return json_dic


class InvalidAuthError(ProtocolError):
    def __init__(self):
        pass

    def json(self, json_dic):
        json_dic['exception'] = 'invalidAuth'
        # TODO: Really send this message?
        display_message('Incorrect login and/or password', 'error', 5)
        return json_dic


def _is_authenticated(user, password):
    # TODO: Replace with a database back-end
    return (user not in USER_PASSWORD or
            password != _password_hash(USER_PASSWORD[user]))

def _password_hash(password):
    return sha512(password).hexdigest()

def login(user, password):
    if not _is_authenticated(user, password):
        raise InvalidAuthError

    get_session()['user'] = user
    display_message('Hello!')
    return {}

def logout():
    get_session().invalidate()
    # TODO: Really send this message?
    display_message('Bye!')
    return {}

def whoami():
    json_dic = {}
    try:
        json_dic['user'] = get_session().get('user')
    except KeyError:
        # TODO: Really send this message?
        display_message('Not logged in!', type='error', duration=3)
    return json_dic

# TODO: Unittesting
