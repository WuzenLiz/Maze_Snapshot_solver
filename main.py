import sys
import getopt
import time
import base64
from Solver import Mazer_solver, create_compare_image
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
input_path = './maze/maze_for_solve.png'
output_path = './maze/solved_maze.png'
compare_path = './maze/compare_image.png'


def Get_image(width, height):
    """Setting webdriver"""
    WDoptions = Options()
    WDoptions.add_argument('--headless')
    WDoptions.add_argument('--disable-gpu')
    driver = webdriver.Chrome(
        './Webdriver/chromedriver.exe', options=WDoptions)
    driver.get("https://keesiemeijer.github.io/maze-generator/")
    """Prepare and generate maze"""
    # maze width input
    print("Generate Maze", width, "*", height)
    maze_w = driver.find_element_by_xpath(
        "//input[@name='width' and @value='20']")
    driver.execute_script(
        "arguments[0].setAttribute('value', arguments[1])", maze_w, width)
    # maze height input
    maze_h = driver.find_element_by_xpath(
        "//input[@name='height' and @value='20']")
    driver.execute_script(
        "arguments[0].setAttribute('value', arguments[1])", maze_h, height)
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
    maze_img_path = driver.find_element_by_xpath(
        "//canvas[@id='maze']")
    js = "return arguments[0].toDataURL('image/png').substring(21)"
    maze_img_to_base64 = driver.execute_script(js, maze_img_path)
    maze_img = base64.b64decode(maze_img_to_base64)
    im = Image.open(BytesIO(maze_img))
    im.save(input_path, quality=100, subsampling=0)
    driver.close()


def main(argv):
    h = w = 40
    try:
        opts, args = getopt.getopt(
            argv, "w:h:?", ["Width=", "Height=", "width=", "height="])
    except getopt.GetoptError:
        print('main.py -w <Maze Width : default = 40, max = 200> -h <Maze Height : default = 40, max = 200>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-?':
            print(
                'main.py -w <Maze Width : default = 40, max = 200> -h <Maze Height : default = 40, max = 200>')
            print("Made by Hoang Anh Nguyen - 2020")
            sys.exit()
        elif opt in ("-w", "--Width", "--width"):
            w = arg
        elif opt in ("-h", "--Height", "--height"):
            h = arg
        elif opt == '':
            w = h = 40
    t0 = time.time()
    Get_image(w, h)
    """solve the maze"""
    Mazer_solver(input_path, output_path)
    create_compare_image(input_path, output_path, compare_path)
    Image.open(compare_path).show()
    """Time count"""
    t1 = time.time()
    total = t1-t0
    print("Done in:", total, "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
