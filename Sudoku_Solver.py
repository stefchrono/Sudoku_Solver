from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome(r"/Users/StefChrono/Downloads/chromedriver") #open_chrome
driver.maximize_window() #maximize_window
driver.get('https://sudoku.com')
time.sleep(1)
dropdown = driver.find_element_by_class_name('difficulty-label')
dropdown.click()
time.sleep(1)
select_lvl_exp = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div[2]/div[2]/ul/li[4]/a')
select_lvl_exp.click()
time.sleep(2)
table = driver.find_elements_by_css_selector("table.game-table tbody tr")
time.sleep(2)

table_data = {

    1: 'M8.954',
    2: 'M.12 9',
    3: 'M6.698',
    4: 'M15.85',
    5: 'M10.55',
    6: 'M10.96',
    7: 'M3.017',
    8: 'M10.53',
    9: 'M10.89'

}

pre_df = []

for row in table:
    rows = row.find_elements_by_xpath(".//td[contains(@class, 'game-cell')]")
    for little_row in rows:
        if str(little_row.get_attribute("class")) == 'game-cell':
            pre_df.append(0)

        else:
            num_rows = little_row.find_elements_by_xpath(".//div[1]/*[name()='svg']/*[name()='path']")
            for numero in num_rows:
                for number, code in table_data.items():
                    if code == (str(numero.get_attribute("d"))[:6]):
                        pre_df.append(number)

chunks = [pre_df[x:x+9] for x in range(0, len(pre_df), 9)]

#######################################################################

def Solve(Sudo):
    zeros = CheckForEmpty(Sudo)
    if not zeros:
        return True
    else:
        row, col = zeros

    for i in range(1, 10):
        if Validation(Sudo, i, (row, col)):
            Sudo[row][col] = i

            if Solve(Sudo):
                return True

            Sudo[row][col] = 0

    return False

def Validation(Sudo, number, position):
    for i in range(len(Sudo)):
        if Sudo[i][position[1]] == number and position[0] != i:
            return False

    for i in range(len(Sudo[0])):
        if Sudo[position[0]][i] == number and position[1] != i:
            return False

    square_x = position[1] // 3
    square_y = position[0] // 3

    for i in range(square_y*3, square_y*3 + 3):
        for j in range(square_x*3, square_x*3 + 3):
            if Sudo[i][j] == number and (i, j) != position:
                return False
    return True

def CheckForEmpty(Sudo):
    for i in range(len(Sudo)):
        for j in range(len(Sudo[0])):
            if Sudo[i][j] == 0:
                return (i, j)

    return None


original = list(map(list, chunks))

Solve(chunks)
print(chunks)

numpad = driver.find_elements_by_class_name("numpad-item")
total_cells = driver.find_elements_by_class_name("game-cell")

for row_number, row_values in enumerate(original):
        for row_value_position, actual_value in enumerate(row_values):
            if actual_value == 0:
                total_cells[row_number*9 + row_value_position].click()
                numpad[chunks[row_number][row_value_position] - 1].click()
