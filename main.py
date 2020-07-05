from Solver import Mazer_solver
from selenium import webdriver
from PIL import Image
from selenium.webdriver.common.keys import Keys
from io import BytesIO
import time
Image.MAX_IMAGE_PIXELS = 933120000
input_path = './maze/maze_for_solve.png'
output_path = './maze/solved_maze.png'
"""Setting webdriver"""
driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://keesiemeijer.github.io/maze-generator/")

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
maze_s_e = driver.find_element_by_xpath(
    "//select[@id='entry' and @name='entry']")
driver.execute_script(
    "arguments[0].setAttribute('value', 'vertical')", maze_s_e)
# click on
driver.find_elements_by_id("create-maze")[0].click()
time.sleep(1)
"""Get maze image"""
maze_img_snapshot = driver.find_elements_by_xpath("//canvas[@id='maze']")
time.sleep(2)
im = maze_img_snapshot[0].screenshot_as_png
maze_img = Image.open(BytesIO(im))
maze_img.save(input_path)
driver.close()
"""solve the maze"""
Mazer_solver(input_path, output_path)
