from Solver import Mazer_solver
from selenium import webdriver  
from PIL import Image
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from io import BytesIO
import time
Image.MAX_IMAGE_PIXELS = 933120000

"""Setting webdriver"""
driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://www.mazegenerator.net/")

"""Prepare and generate maze"""
maze_width = maze_height = 50
maze_w = driver.find_element_by_id("S1WidthTextBox")
driver.execute_script("arguments[0].setAttribute('value', '25')", maze_w)
maze_h = driver.find_element_by_id("S1HeightTextBox")
driver.execute_script("arguments[0].setAttribute('value', '25')", maze_h)
Click_On_Generate_Button = driver.find_elements_by_xpath("//input[@name='GenerateButton' and @value='Generate']")[0]
Click_On_Generate_Button.click()
time.sleep(5)
"""Get maze image"""
path1 = './maze/maze_for_solve.png'
maze_img_snapshot = driver.find_elements_by_id("MazeDisplay")[0].screenshot_as_png
maze_img=Image.open(BytesIO(maze_img_snapshot))
maze_img.save(path1)
driver.close()
"""solve the maze"""
path2 = './maze/solved_maze.png'
Mazer_solver(path1,path2)


