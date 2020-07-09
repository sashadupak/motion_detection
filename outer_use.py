from low_func import *
import os

in_dir = '/home/alexander/Документы/camera/raw/0904/'
out_dir = '/home/alexander/Документы/camera/raw/1752/'
d = os.listdir(in_dir)

for file in d:
    #print(in_dir + str(file))
    if os.path.isfile(in_dir + str(file)):
        run(in_dir + str(file), out_dir, visible=False)
print('The end.')