"""
CalPolyClassFinder is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

CalPolyClassFinder is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU General Public License for more details.

You should have received a copy of the GNU General Public License 
along with Cal Poly Class Finder. If not, see <https://www.gnu.org/licenses/>.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
import time
"""
TODO: Add notifications sent to my phone with the current sections that are open for CSC
TODO: Eventually add everything to sqlite3 database and have it update every hour using raspberry pi
TODO: Make it so that it can search for multiple majors at once
"""

CLASS_SEARCH_LINK = 'https://cmsweb.pscs.calpoly.edu/psc/CSLOPRD/EMPLOYEE/SA/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL'

def scrapePage():
    # Starts a new search
    wait = WebDriverWait(driver, 2)
    main_table = driver.find_element(by=By.ID, value='ACE_DERIVED_CLSRCH_GROUP6')

    'PSGROUPBOXWBO'
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find_all('table', id='ACE_DERIVED_CLSRCH_GROUP6')
    dfs = pd.read_html(str(table))
    with open('classes.txt', 'w') as f:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            dfs[0]
    #with open('classes.txt', 'w') as f:
    #    for i in dfs[0].values.tostring():
    #        f.write(np.fromstring(i, dtype=int))
            
    #new_search_button = wait.until(EC.presence_of_element_located((By.NAME, 'CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH$3$'))).click()


# TODO Make it choose the latest term
def getClasses(major, catalog_number=1, termtime='2236'):
    """Must be on main Cal Poly search page, if so chooses a major and views all clases for that major

    major: tuple returned from getMajor()
    """
    isSTR = False
    if type(major) == str:
        isSTR = True
    Select(driver.find_element(by=By.NAME, value='CLASS_SRCH_WRK2_INSTITUTION$31$')).select_by_index(1)

    # Waits for page to update once you click CalPoly SLO
    while True:
        try:
            term = driver.find_element(by=By.NAME, value='SLO_SS_DERIVED_STRM')
            term.clear()
            term.send_keys(termtime)
            print(term.get_attribute('value'))
            break
        except:
            pass

    # Don't ask why this works just fucking accept it
    wait = WebDriverWait(driver, 2)
    subject = Select(wait.until(EC.element_to_be_clickable((By.ID, 'SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))))
    if isSTR == True:
        subject.select_by_value(major)
    else:
        subject.select_by_index(major)
    time.sleep(2)
    subject = Select(driver.find_element(by=By.NAME, value='SSR_CLSRCH_WRK_SUBJECT_SRCH$0'))
    if isSTR == True:
        subject.select_by_value(major)
    else:
        subject.select_by_index(major)
    course_number_select = Select(driver.find_element(by=By.NAME, value='SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$1'))
    course_number_select.select_by_index(2)
    course_number = driver.find_element(by=By.NAME, value='SSR_CLSRCH_WRK_CATALOG_NBR$1').send_keys(catalog_number)
    submit_button = driver.find_element(by=By.NAME, value='CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH').click()

    # Wait until a element has loaded on the page
    wait.until(EC.presence_of_element_located((By.NAME, 'CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH$3$')))

driver = webdriver.Chrome()
driver.get(CLASS_SEARCH_LINK)
title = driver.title
print(title)
getClasses("CSC", 500)
scrapePage()

while True:
    pass
driver.quit()
