from selenium import webdriver 

uname ='012583'
password = 'aadp$19870120'

url= 'http://ossportal/crms/login.html'

driver = webdriver.Chrome('chromedriver')
driver.get(url)

driver.find_element_by_name("txtuser").send_keys(uname)
driver.find_element_by_name("txtpwd").send_keys(password)

driver.find_element_by_name("login").click()