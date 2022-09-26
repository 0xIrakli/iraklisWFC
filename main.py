from PIL import Image
import random as rand
import os
import numpy as np
from copy import deepcopy
import sys
sys.setrecursionlimit(5000)

history = []
PATH = 'images/'
W = 5
i = 0
grid = []

def format(l, n):
    return np.array(list(chunks(l, n)))

def chunks(list_, n):
    for i in range(0, len(list_), n):
        yield list_[i:i + n]

def import_images(dir_):
    images = []
    for path in os.listdir(dir_):
        img = Image.open(dir_+path)
        for i in range(0, 270, 90):
            images.append(img.rotate(i))
    return images

def generate_grid(s, images):
    grid = []
    for y in range(s):
        grid.append([])
        for x in range(s):
            grid[y].append(images.copy())
    return grid

def conv(img):
    return format(list(img.getdata()), img.width)

func = {
    (0,-1): lambda arr: [list(a[ 0]) for a in np.rot90(arr)],
    (1, 0): lambda arr: [list(a[-1]) for a in arr],
    (0, 1): lambda arr: [list(a[-1]) for a in np.rot90(arr)],
    (-1,0): lambda arr: [list(a[ 0]) for a in arr],
}

darkside_func = {
    (0,-1): lambda arr: [list(a[-1]) for a in np.rot90(arr)],
    (1, 0): lambda arr: [list(a[ 0]) for a in arr],
    (0, 1): lambda arr: [list(a[ 0]) for a in np.rot90(arr)],
    (-1,0): lambda arr: [list(a[-1]) for a in arr],
}

def collapse(x, y, i):
    f = 0
    for y_ in range(len(grid)):
        for x_ in range(len(grid[y_])):
            f += len(grid[y_][x_])
    if f == len(grid)*len(grid[y_]):
        print('done')
        quit()
    if i >= 500:
        print('xuina')
        quit()
    if len(grid[y][x]) != 1:
        this = grid[y][x]
        rem = []
        for X, Y in func.keys():
            try:
                if len(grid[y+Y][x+X]) == 1:
                    i2 = grid[y+Y][x+X][0]
                    for i1 in this:
                        if func[(X, Y)](conv(i1)) != darkside_func[(X, Y)](conv(i2)):
                            rem.append(i1)
            except: pass
        for r in rem:
            if r in this:
                this.remove(r)
        if len(this) <= 1:
            for i, yy in enumerate(deepcopy(history[-1])):
                grid[i] = yy
            history.pop()
            collapse(x, y, i+1)
        else:
            grid[y][x] = [rand.choice(this)]
    for y_ in range(W):
        for x_ in range(W):
            if len(grid[y_][x_]) == 0:
                print('AAAAAAAAAAAA')
            if len(grid[y_][x_]) == 1:
                im.paste(grid[y_][x_][0], (x_*25, y_*25))
    history.append(deepcopy(grid))
    im.save('test.png')
    while True:
        X, Y = rand.choice(list(func.keys()))
        if 0 <= x+X < W and 0 <= y+Y < W:
            collapse(x+X, y+Y, i+1)
            break

im = Image.new('RGB', (W*25, W*25), (51, 51, 51))
images = import_images('images/')
grid = generate_grid(W, images)
choice = rand.choice(images)
x, y = rand.randrange(0, W), rand.randrange(0, W)
collapse(x, y, 0)
im.show()