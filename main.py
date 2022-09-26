from PIL import Image
import random as rand
import os
import numpy as np
from copy import deepcopy

history = []
PATH = 'images/'
W = 20
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

def lowest_entropy():
    data = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            l = len(grid[y][x])
            if l > 1:
                if l not in data:
                    data[l] = []
                data[l].append((x, y))
    for key in data:
        if len(data[key]) == 0:
            data[key] = [1]*100
    return rand.choice(data[min(list(data.keys()))])

def update(x, y, choice):
    grid[y][x] = [choice]
    for X, Y in func.keys():
        try:
            rem = []
            for im in grid[y+Y][x+X]:
                if func[X, Y](conv(choice)) != darkside_func[X, Y](conv(im)):
                    rem.append(im)
            for img in rem:
                if img in grid[y+Y][x+X]:
                    grid[y+Y][x+X].remove(img)
        except:pass
            
im = Image.new('RGB', (W*25, W*25), (51, 51, 51))
images = import_images('images/')
grid = generate_grid(W, images)
x, y = rand.randrange(W), rand.randrange(W)
choice = rand.choice(images.copy())
update(x, y, choice)

for x in range(100):
    print(lowest_entropy())
    x, y = lowest_entropy()
    print(x, y)
    update(x, y, rand.choice(grid[y][x]))
    for y_ in range(W):
        for x_ in range(W):
            if len(grid[y_][x_]) == 0:
                print('AAAAAAAAAAAA')
            if len(grid[y_][x_]) == 1:
                im.paste(grid[y_][x_][0], (x_*25, y_*25))
    im.save('test.png')
im.show()