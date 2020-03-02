from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8888')

        # She notices the page title and header mention to-do lists
        self.assertIn('Online courses', self.browser.title)
        #self.fail('Finish the test!')
    def test_login_form(self):
        self.browser.get('http://localhost:8888')
        inputbox_username = self.browser.find_element_by_name('username')
        self.assertEqual(
                inputbox_username.get_attribute('placeholder'),
                'login'
        )
        inputbox_password = self.browser.find_element_by_name('password')
        self.assertEqual(
                inputbox_password.get_attribute('placeholder'),
                'password'
        )
       

if __name__ == '__main__':
    unittest.main(warnings='ignore')
