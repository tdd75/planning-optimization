import random
import string
import os
import glob

filepaths = glob.glob("D:\Desktop\*")
print(filepaths)

# for filepath in filepaths:
#     letters = string.ascii_letters
#     digits = string.digits
#     pool = letters + digits
#     l = list(pool)
#     random.shuffle(l)
#     pool = ''.join(l)
#     name = ''.join(random.choice(pool) for i in range(10))
#     os.rename(filepath, 'D:\\Pictures\\Wallpaper\\' + name + '.jpg')