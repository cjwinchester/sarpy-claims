from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta
import smtplib

today = date.today()
weekago = today - timedelta(days=7)

print weekago

def num_padder(x):
    if len(str(x)) == 1:
        return "0" + str(x)
    else:
        return str(x)
        
beginstring = num_padder(weekago.month) + "/" + num_padder(weekago.day) + "/" + str(weekago.year)

endstring = num_padder(today.month) + "/" + num_padder(today.day) + "/" + str(today.year)

driver = webdriver.Chrome()
driver.get("http://www.sarpy.com/claims")

assert "Sarpy County" in driver.title
print "Connected!"

elem = driver.find_elements_by_class_name("igte_EditInContainer")

driver.execute_script('var elm = document.getElementsByClassName("igte_EditInContainer"); elm[0].removeAttribute("readonly"); elm[1].removeAttribute("readonly");')

begin = elem[0]
end = elem[1]

begin.click()
begin.send_keys(beginstring)

end.click()
end.send_keys(endstring)

driver.find_element_by_id("MainContent_btnFinish__3").click()

page = driver.page_source
soup = BeautifulSoup(page)

driver.close()

f = open('sarpy_claims.txt', 'ab')

table = soup.findAll('table')[10]

counter = 1

for row in table.findAll('tr'):
    col = row.findAll('td')
    date = col[0].string.strip()
    dept = col[1].string.strip()
    payee = col[2].string.strip()
    print payee
    amt = col[3].string.strip().replace('$','')
    descrip = col[4].string.strip()
    rec = (date, dept, payee, amt, descrip)
    f.write("|".join(rec) + "\n")
    counter += 1

print str(counter) + ' new Sarpy claims this week ...'
    
f.flush()
f.close()