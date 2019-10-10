from sys import platform
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time


if platform == "linux":
	# Linux chrome driver
	browser_driver_path = './chromedriver'
else:
	# Windows Chrome driver
	browser_driver_path = './chromedriver.exe'

MAX_WAIT = 4 	

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Chrome(browser_driver_path)

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
		# Boatcow has heard about a cool new online to-do app. She goes 
		# to check out its homepage.
		self.browser.get(self.live_server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)		

		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		# Boatcow types "Nod my head" into a text box 
		inputbox.send_keys('Nod my head')

		# When she hits enter, the page updates, and now the page lists '1: Nod my head' as an item in a to-do list table
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Nod my head')
		

		# There is still a text box inviting Boatcow to add another item. She enters 'Ask for food'
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Ask for food')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on her list
		self.wait_for_row_in_list_table('2: Ask for food')
		self.wait_for_row_in_list_table('1: Nod my head')

		# Satisfied, she goes back to the boat.
		

		# Boatcow wonders wehter the site will remember her list. The she sees
		# that the site has generated a unique URL for her -- there is some 
		# explanatory text to that effect
		# Boatcow visits that URL - her to-do list is still there.

		

	def test_multiple_users_can_start_lists_at_different_urls(self):
		# Boatcow starts a new to-do list
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Nod my head')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Nod my head')

		# She notices that her list has a unique URL
		boatcow_list_url = self.browser.current_url
		self.assertRegex(boatcow_list_url, '/lists/.+')

		# Now a new user, Peepeepoopoo, comes along to the site.

		## We use a new browser session to make sure that no information 
		## of Boatcow's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Chrome(browser_driver_path)

		# Peepeepoopoo visits the home page. There is no sign of Boatcow's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Nod my head', page_text)
		self.assertNotIn('Ask for food', page_text)

		# Peepeepoopoo starts a new list by entering a new item. He 
		# is less orthodox than Boatcow...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Dig a hole in the yard')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Dig a hole in the yard')

		# Peepeepoopoo gets his own unique URL
		peepeepoopoo_list_url = self.browser.current_url
		self.assertRegex(peepeepoopoo_list_url, 'lists/.+')
		self.assertNotEqual(peepeepoopoo_list_url, boatcow_list_url)

		# Again, there is no trace of Boatcow's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Nod my head', page_text)
		self.assertIn('Dig a hole in the yard', page_text)

		# Satisifed the return to thier duty.


