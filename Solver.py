from maze import Maze
from PIL import Image, ImageDraw, ImageFont
from AStar import solve
import numpy as np
import time
Image.MAX_IMAGE_PIXELS = None


def Mazer_solver(input_file, output_file):
    # Load Image
    im = Image.open(input_file)
    # Create the maze (and time it) - for many mazes this is more time consuming than solving the maze
    print("\nLoad node from image to Maze")
    t0 = time.time()
    maze = Maze(im)
    t1 = time.time()
    print("Node Count:", maze.count)
    total = t1-t0
    print("Time elapsed:", total, "\n")

    # Create and run solver
    title = "A Star Algo"
    print("Starting Solve:", title)

    t0 = time.time()
    [result, stats] = solve(maze)
    t1 = time.time()

    total = t1-t0

    # Print solve stats
    print("Nodes explored: ", stats[0])
    if (stats[2]):
        print("Path found, length", stats[1])
    else:
        print("No Path Found")
    print("Time elapsed: ", total, "\n")

    print("Saving Image")
    im = im.convert("RGB")
    impixels = im.load()

    resultpath = [n.Position for n in result]

    length = len(resultpath)

    for i in range(0, length - 1):
        a = resultpath[i]
        b = resultpath[i+1]

        # Blue - red
        r = int((i / length) * 255)
        px = (r, r-r//2, 255 - r)

        if a[0] == b[0]:
            # Ys equal - horizontal line
            for x in range(min(a[1], b[1]), max(a[1], b[1])):
                impixels[x, a[0]] = px
        elif a[1] == b[1]:
            # Xs equal - vertical line
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                impixels[a[1], y] = px
    im.save(output_file, quality=100, subsampling=0)


def resize_for_better_look(input_file, text):
    im = Image.open(input_file)
    w, h = im.size
    newsize = (w*5, h*5)
    im = im.resize(newsize)
    new_im_size = (w*5+10, h*5+35)
    new_im = Image.new('RGB', new_im_size)
    new_im.paste(im, (5, 30))
    draw = ImageDraw.Draw(new_im)
    font = ImageFont.truetype('arial.ttf', 20)
    draw.text((new_im_size[1]/5, 5), text, (255, 255, 255), font=font)
    new_im.save(input_file, quality=100, subsampling=0)


def create_compare_image(input_file, output_file, compare_file):
    resize_for_better_look(input_file, "Original Maze")
    resize_for_better_look(output_file, "Solved Maze")
    imgs = [Image.open(i) for i in [input_file, output_file]]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    widths, heights = zip(*(i.size for i in imgs))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))
    # Place first image
    new_im.paste(imgs[0], (0, 0))

    # Iteratively append images in list horizontally
    hoffset = 0
    for i in range(1, len(imgs), 1):
        hoffset = imgs[i-1].size[0]+hoffset
        new_im.paste(imgs[i], (hoffset, 0))
    new_im.save(compare_file, quality=100, subsampling=0)
