from sys import platform
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import unittest
import time


if platform == "linux":
	# Linux chrome driver
	broser_driver_path = './chromedriver'
else:
	# Windows Chrome driver
	broser_driver_path = './chromedriver.exe'

MAX_WAIT = 10 	

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Chrome(broser_driver_path)

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

	def test_can_start_a_list_and_retrieve_it_later(self):
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
		self.wait_for_row_in_list_table('1: Nod my head')
		self.wait_for_row_in_list_table('2: Ask for food')

		# Boatcow wonder wehter the site will remember her list. The she sees
		# that the site has generated a unique URL for her -- there is some 
		# explanatory text to that effect
		self.fail("Finish the test!")

		# Boatcow visits that URL - her to-do list is still there.
