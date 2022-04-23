from selenium import webdriver
import requests

chrome_driver_path = '/Users/odinakaarochukwu/Documents/chromedriver'


level = input("What difficulty do you want the board to be? 1 - Easy and 4 - Evil ")

driver = webdriver.Chrome(chrome_driver_path)
driver.get(f'https://nine.websudoku.com/?level={level}')

theline = ""
for i in range(0, 9):
    for j in range(0, 9):
        theparent = driver.find_element_by_id(f"c{j}{i}")
        if theparent.find_elements_by_tag_name("input")[0].get_attribute("value") != '':
            theline += theparent.find_elements_by_tag_name("input")[0].get_attribute("value")
        else:
            theline += "."

res = requests.get(f'https://sudoku--api.herokuapp.com/solve-board?sudo={theline}')
response = res.json()["response"]["solution"]

for i in range(0, 9):
    for j in range(0, 9):
        theparent = driver.find_element_by_id(f"c{j}{i}")
        thechild = theparent.find_elements_by_tag_name("input")[0]
        if thechild.get_attribute("value") == '':
            thechild.send_keys(str(response[i][j]))

driver.find_element_by_css_selector(".bs[name='submit']").click()

