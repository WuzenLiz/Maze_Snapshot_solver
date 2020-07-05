from maze import Maze
from PIL import Image
from AStar import solve
import time
Image.MAX_IMAGE_PIXELS = None


def Mazer_solver(input_file, output_file):
    # Load Image
    print("Loading Image")
    im = Image.open(input_file)
    # Create the maze (and time it) - for many mazes this is more time consuming than solving the maze
    print("Load to Maze")
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
    im = im.convert('RGB')
    impixels = im.load()

    resultpath = [n.Position for n in result]

    length = len(resultpath)

    for i in range(0, length - 1):
        a = resultpath[i]
        b = resultpath[i+1]

        # Blue - red
        r = int((i / length) * 255)
        px = (r, 0, 255 - r)

        if a[0] == b[0]:
            # Ys equal - horizontal line
            for x in range(min(a[1], b[1]), max(a[1], b[1])):
                impixels[x, a[0]] = px
        elif a[1] == b[1]:
            # Xs equal - vertical line
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                impixels[a[1], y] = px

    im.save(output_file)
