#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file mymail_parser.py
@author Sam Freeside <snovvcrash@protonmail[.]ch>
@date 2018-07

@brief Парсер email-адресов соц. сети "Мой мир@Mail.Ru".

@license
Copyright (C) 2018 Sam Freeside

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endlicense
"""

import time
import csv
import sys

from random import uniform, randint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm

from credentials import mymail

GECKODRIVER_PATH = ' '  # указать путь к веб-драйверу FF'а
HEADLESS = True  # изменить на "False", чтобы в процессе выполнения открылось окно браузера

SEARCH_QUERY = 'https://my.mail.ru/my/search_people?&name=John Doe'  # указать поисковой запрос


def get_driver():
	options = Options()
	options.set_headless(headless=HEADLESS)

	driver = webdriver.Firefox(
		firefox_options=options,
		executable_path=GECKODRIVER_PATH
	)

	# _driver.set_window_size(1000, 1080)

	return driver


def mymail_sign_in(driver, login, password):
	driver.get('https://my.mail.ru')
	time.sleep(uniform(1, 2))

	login_form = driver.find_element_by_xpath("//input[@class='l-loginform_row_label_input'][@name='Login']")
	password_form = driver.find_element_by_xpath("//input[@class='l-loginform_row_label_input'][@name='Password']")

	login_form.send_keys(login)
	password_form.send_keys(password)

	sign_in_button = driver.find_element_by_xpath("//input[@class='ui-button-main'][@type='submit']")
	sign_in_button.submit()
	time.sleep(uniform(1, 2))


def get_emails(driver, query, count):
	driver.get(query)
	time.sleep(uniform(3, 4))

	last_height = driver.execute_script("return document.body.scrollHeight")

	try_again = True
	for i in tqdm(range(count), ncols=80, unit='scroll', desc='\talmost done'):
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight - {});".format(randint(1000, 1100)))
		time.sleep(uniform(3, 4))

		new_height = driver.execute_script("return document.body.scrollHeight")

		if new_height == last_height:
			if try_again:
				try_again = False
				driver.execute_script("window.scrollTo(0, 0);")
				time.sleep(uniform(3, 4))
				continue
			break

		last_height, try_again = new_height, True

	emails = set()
	links = driver.find_elements_by_xpath("//a[starts-with(@href, '/mail/')]")

	for link in links:
		name = link.text
		email = link.get_attribute('data-email')
		if name and email:
			emails.add(('https://my.mail.ru/mail/' + email, email, name))

	return emails


def write_csv(emails):
	with open('out.csv', 'w', encoding='utf-8') as f:
		writer = csv.writer(f, lineterminator='\n')
		writer.writerow(('url', 'email', 'name'))
		writer.writerows(emails)


def main():
	if len(sys.argv) != 2:
		print('Usage: python3 {} <number_of_scrolls>\n(1 scroll ~ 8 emails)'.format(sys.argv[0]))
		sys.exit(1)

	try:
		number_of_scrolls = int(sys.argv[1])
	except ValueError:
		print('number_of_scrolls: Invalid input type')
		sys.exit(1)

	print('[*] Initializing webdriver... ')
	driver = get_driver()
	print('[+] Done.')

	print('[*] Signing in... ')
	mymail_sign_in(driver, mymail.login, mymail.password)
	print('[+] Done.')

	print('[*] Collecting emails... ')
	emails = get_emails(driver, SEARCH_QUERY, number_of_scrolls)
	print('[+] Done.')

	driver.quit()

	if emails:
		print('[*] Creating .csv file... ')
		write_csv(emails)
		print('[+] Done.')

		print('\nParsed {} emails, result file: out.csv'.format(len(emails)))
	else:
		print('[-] Failure: server timeout or bad search query')


if __name__ == '__main__':
	main()
