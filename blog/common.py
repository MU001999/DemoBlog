# -*- coding: utf-8 -*-
import os
import random
from PIL import Image
import numpy as np


def to_str(unicode_or_str):
    if isinstance(unicode_or_str, unicode):
        return unicode_or_str.encode('utf-8')
    else:
        return unicode_or_str


def to_unicode(unicode_or_str):
    if isinstance(unicode_or_str, str):
        return unicode_or_str.encode('utf-8')
    else:
        return unicode_or_str


def avatar_gen(username):
    image = np.array([255]*10000, dtype='int')
    image = image.reshape([100, 100])
    image = Image.fromarray(image)
    image = image.convert('RGB')
    image = np.asarray(image)
    image = np.copy(image)
    for i in range(10):
        for j in range(10):
            if random.randint(0, 1) or i <= 1 or i >= 8 or j <= 1 or j >= 8:
                continue
            for p in range(3):
                target = random.randint(0, 255)
                for x in range(i*10, i*10+10):
                    for y in range(j*10, j*10+10):
                        image[x][y][p] = target
    image = Image.fromarray(image, 'RGB')
    if not os.path.isdir(os.path.join('blog', 'static', 'imgs', 'users')):
        os.mkdir(os.path.join('blog', 'static', 'imgs', 'users'))
    if not os.path.isdir(os.path.join('blog', 'static', 'imgs', 'users', username)):
        os.mkdir(os.path.join('blog', 'static', 'imgs', 'users', username))
    image.save(os.path.join('blog', 'static', 'imgs', 'users', username, 'default.jpg'))
    return os.path.join(username, "default.jpg")
