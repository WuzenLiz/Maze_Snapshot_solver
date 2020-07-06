from Fibonacci_Heap import FibHeap
from priority_queue import FibPQ


def solve(maze):
    width = maze.width
    total = maze.width * maze.height

    start = maze.start
    startpos = start.Position
    end = maze.end
    endpos = end.Position

    visited = [False] * total
    prev = [None] * total

    infinity = float("inf")
    distances = [infinity] * total

    unvisited = FibPQ()

    nodeindex = [None] * total

    distances[start.Position[0] * width + start.Position[1]] = 0
    startnode = FibHeap.Node(0, start)
    nodeindex[start.Position[0] * width + start.Position[1]] = startnode
    unvisited.insert(startnode)

    count = 0
    completed = False

    while len(unvisited) > 0:
        count += 1

        n = unvisited.removeminimum()

        u = n.value
        upos = u.Position
        uposindex = upos[0] * width + upos[1]

        if distances[uposindex] == infinity:
            break

        if upos == endpos:
            completed = True
            break

        for v in u.Neighbours:
            if v != None:
                vpos = v.Position
                vposindex = vpos[0] * width + vpos[1]

                if visited[vposindex] == False:
                    d = abs(vpos[0] - upos[0]) + abs(vpos[1] - upos[1])
                    newdistance = distances[uposindex] + d

                    remaining = abs(vpos[0] - endpos[0]) + \
                        abs(vpos[1] - endpos[1])

                    if newdistance < distances[vposindex]:
                        vnode = nodeindex[vposindex]

                        if vnode == None:
                            vnode = FibHeap.Node(newdistance + remaining, v)
                            unvisited.insert(vnode)
                            nodeindex[vposindex] = vnode
                            distances[vposindex] = newdistance
                            prev[vposindex] = u
                        else:
                            unvisited.decreasekey(
                                vnode, newdistance + remaining)
                            distances[vposindex] = newdistance
                            prev[vposindex] = u

        visited[uposindex] = True

    from collections import deque

    path = deque()
    current = end
    while (current != None):
        path.appendleft(current)
        current = prev[current.Position[0] * width + current.Position[1]]

    return [path, [count, len(path), completed]]
