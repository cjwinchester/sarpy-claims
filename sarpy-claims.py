from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.sarpy.com/claims")

assert "Sarpy County" in driver.title
elem = driver.find_elements_by_class_name("igte_EditInContainer")

driver.execute_script('var elm = document.getElementsByClassName("igte_EditInContainer"); elm[0].removeAttribute("readonly"); elm[1].removeAttribute("readonly");')

begin = elem[0]
end = elem[1]

begin.click()
begin.send_keys('1/1/2013')

end.click()
end.send_keys('1/15/2013')

driver.find_element_by_id("MainContent_btnFinish__3").click()

page = driver.page_source
soup = BeautifulSoup(page)

driver.close()

table = soup.findAll('table')[10]

f = open('claims.txt', 'wb')

for row in table.findAll('tr'):
    col = row.findAll('td')
    date = col[0].string.strip()
    dept = col[1].string.strip()
    payee = col[2].string.strip()
    amt = col[3].string.strip().replace('$','')
    descrip = col[4].string.strip()
    rec = (date, dept, payee, amt, descrip)
    f.write("|".join(rec) + "\n")
	
f.flush()
f.close()
