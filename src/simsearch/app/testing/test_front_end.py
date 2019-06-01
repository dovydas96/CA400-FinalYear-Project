# import time
# import os
#
#
# def test_frontend_buttons_and_functions(webdriver):
#
#     webdriver.get('http://127.0.0.1:5000/register')
#     webdriver.find_element_by_id("username").send_keys('test1')
#     webdriver.find_element_by_id("email").send_keys('test1@example.com')
#     webdriver.cu
#     webdriver.find_element_by_id("password").send_keys('test1')
#     webdriver.find_element_by_id("password2").send_keys('test1')
#     webdriver.find_element_by_id("submit").click()
#     time.sleep(1)
#     webdriver.find_element_by_id("username").send_keys('test1')
#     webdriver.find_element_by_id("password").send_keys('test1')
#     webdriver.find_element_by_id("submit").click()
#     time.sleep(1)
#     webdriver.find_element_by_id("logout").click()
#     time.sleep(1)
#     webdriver.find_element_by_id("username").send_keys('test1')
#     webdriver.find_element_by_id("password").send_keys('test1')
#     webdriver.find_element_by_id("submit").click()
#     webdriver.find_element_by_id("upload").send_keys(os.getcwd()+"/app/testing/test.jpeg")
#     webdriver.find_element_by_id("submit").click()
#     time.sleep(1)
#     webdriver.find_element_by_id("upvote").click()
#     time.sleep(1)
#     webdriver.find_element_by_id("profile").click()
#     webdriver.find_element_by_id("search").click()
#     webdriver.find_element_by_id("downvote").click()
#     time.sleep(1)
#     webdriver.find_element_by_id("profile").click()
#     webdriver.find_element_by_id("delete_account").click()
#     time.sleep(1)
#     time.sleep(1)
