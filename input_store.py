import time
import os
import Image


input_dict = {}
current_time = 0
while True:
    os.system("scrot -u %s.png", current_time)
    current_img = Image.open("%s.png", current_time)
    input_dict[(current_img,REPLACE_ME_WITH_NAME_OF_SET)] = current_time #replace REPLACE_ME-WITH_NAME_OF_SET with the name of the set of keyboard actions
    current_time += 0.5
    time.sleep(0.5)
