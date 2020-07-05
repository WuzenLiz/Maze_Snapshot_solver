from Solver import Mazer_solver
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from io import BytesIO
import time
import base64

"""Setting webdriver"""
driver = webdriver.Chrome('./Webdriver/chromedriver')
t0 = time.time()
driver.get("https://keesiemeijer.github.io/maze-generator/")
input_path = './maze/maze_for_solve.png'
output_path = './maze/solved_maze.png'

"""Prepare and generate maze"""
# maze width input
maze_w = driver.find_element_by_xpath(
    "//input[@name='width' and @value='20']")
driver.execute_script("arguments[0].setAttribute('value', '40')", maze_w)
# maze height input
maze_h = driver.find_element_by_xpath(
    "//input[@name='height' and @value='20']")
driver.execute_script("arguments[0].setAttribute('value', '40')", maze_h)
# fix wall size
maze_wall_size = driver.find_element_by_id("wall-size")
driver.execute_script(
    "arguments[0].setAttribute('value', '1')", maze_wall_size)
# select for start/end at top/bottop
Select(driver.find_element_by_xpath(
    "//select[@id='entry' and @name='entry']")).select_by_value('vertical')
# click on
driver.find_elements_by_id("create-maze")[0].click()

"""Get maze image"""
maze_img_path = driver.find_element_by_xpath("//canvas[@id='maze']")
js = "return arguments[0].toDataURL('image/png').substring(21)"
maze_img_to_base64 = driver.execute_script(js, maze_img_path)
maze_img = base64.b64decode(maze_img_to_base64)
with open(input_path, 'wb') as f:
    f.write(maze_img)
driver.close()


"""solve the maze"""
Mazer_solver(input_path, output_path)
t1 = time.time()
total = t1-t0
print("Tổng thời gian thực hiện:", total, "\n")
