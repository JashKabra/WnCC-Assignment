from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.chrome.options import Options
import csv
import os
from webdriver_manager.chrome import ChromeDriverManager
import time

with open('States.csv','r') as file:
    states=list(csv.reader(file,skipinitialspace=True))

for x in range(len(states)):
    print("{}-{}".format(states[x][0],x+1))

val=input("Enter the index of the state of which you want the cases: ")
if(int(val)<1 or int(val)>36):
    print("You entered an out of range value.")
    exit()
current_state=states[int(val)-1][0]
print("You chose the state {}.".format(current_state))

chrome_options = Options()
chrome_options.add_argument("--log-level=OFF")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument("--headless")

os.environ['WDM_LOG_LEVEL'] = '0'
driver = webdriver.Chrome(ChromeDriverManager(cache_valid_range=0).install(),options=chrome_options)
driver.get('https://www.covid19india.org/state/'+states[int(val)-1][1])
driver.implicitly_wait(5)

try:
    buttonIsPresent=driver.find_elements_by_css_selector(".button.fadeInUp").__len__()==0
    if(not buttonIsPresent):
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.fadeInUp"))
        )
        element.click()
    
    element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.CLASS_NAME, "district-bar-left"))
    )
    s=(element.text).splitlines()
except:
    print("The webpage took too long to load. Please try again.")

finally:
    driver.quit()

if(len(s)<=1):
    print("District wise data not available in this state.")
    exit()

try:
    file_name=current_state+'.csv'
    with open(file_name,'w') as file:
        writer=csv.writer(file,lineterminator='\n')
        writer.writerow(['District','Cases'])
        for x in range(int(len(s)/2)):
            writer.writerow([s[2*(x+1)],s[2*x+1]])
        os.system('start excel.exe "{}"'.format((file_name)))
        print("{}.csv file is saved in your directory.".format(current_state))
        time.sleep(1)
except:
    print("Please close already open file and try again.")
    time.sleep(1)
