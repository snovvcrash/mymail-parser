#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple

LOGIN = ' '     # указать логин
PASSWORD = ' '  # указать пароль


Credentials = namedtuple('Credentials', [
	'login',
	'password'
])

mymail = Credentials(LOGIN, PASSWORD)
