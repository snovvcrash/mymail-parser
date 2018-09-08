#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

LOGIN = 'LOGIN'        # указать логин
PASSWORD = 'PASSWORD'  # указать пароль


Credentials = namedtuple('Credentials', [
	'login',
	'password'
])

mymail = Credentials(LOGIN, PASSWORD)
