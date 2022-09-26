from PIL import Image
import random as rand
import os
import numpy as np
from copy import deepcopy

history = []
PATH = 'images/'
W = 40
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
    print(len(data[min(list(data.keys()))]))
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
blank = Image.new('RGB', (25, 25), (51, 51, 51))
images = import_images('images/')
grid = generate_grid(W, images)
x, y = rand.randrange(W), rand.randrange(W)
choice = rand.choice(deepcopy(images))
history = []
update(x, y, choice)
avoid = ''
while True:
    x, y = lowest_entropy()
    count = 0
    f = False
    copy = deepcopy(grid[y][x])
    try:
        copy.remove(avoid)
    except:pass
    
    update(x, y, rand.choice(copy))
    for y_ in range(W):
        for x_ in range(W):
            if len(grid[y_][x_]) == 1:
                count += 1
                im.paste(grid[y_][x_][0], (x_*25, y_*25))
            elif len(grid[y_][x_]) == 0:
                grid = deepcopy(history[-1])
                history.pop()
                f = True
                avoid = grid[y_][x_]
            else:
                im.paste(blank, (x_*25, y_*25))
    if not f:
        if count == W*W:
            print('done')
            break
        history.append(deepcopy(grid))
    im.save('test.png')
im.save('test.png')
im.show()