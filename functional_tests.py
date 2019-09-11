from sys import platform
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


if platform == "linux":
	# Linux chrome driver
	broser_driver_path = './chromedriver'
else:
	# Windows Chrome driver
	broser_driver_path = './chromedriver.exe'

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome(broser_driver_path)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Boatcow has heard about a cool new online to-do app. She goes 
		# to check out its homepage.
		self.browser.get('localhost:8000')

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
		time.sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Nod my head', [row.text for row in rows])

		# There is still a text box inviting Boatcow to add another item. She enters 'Ask for food'
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Ask for food')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		# The page updates again, and now shows both items on her list
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Nod my head', [row.text for row in rows])
		self.assertIn('2: Ask for food', [row.text for row in rows])

		# Boatcow wonder wehter the site will remember her list. The she sees
		# that the site has generated a unique URL for her -- there is some 
		# explanatory text to that effect
		self.fail("Finish the test!")

		# Boatcow visits that URL - her to-do list is still there.

if __name__ == '__main__':
	unittest.main()