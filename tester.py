import random
import os
import re
import json
import time
from random import randint

time.sleep(randint(7,10))
with open("token_value.txt", "r") as f:
    token = f.read()
    token_value = token.split(",")
    authorization = token_value[1]

# dir_image = "images/"
# files = os.listdir(dir_image)
# chosen_image = random.choice(files)
#
# print(chosen_image)

# with open("upload_pic_response.txt", "r") as f:
#     photo_id = f.read()
#     tes = photo_id.split(":")
#     des = tes[1].split("}")
#     print(des[0])

f = open('accounts.json', )
users = json.load(f)
happy = random.choice(users)
sad = happy["userID"]
# sad = "1222333"
res = sad.split("d")[1]
# print(res)

random_user = users[0]  # random user selected
random_user_id = random_user["userID"]  # id of the random user selected
random_username = random_user["username"]  # username of the random user selected
search_result_selector = f'''  a[href^="{random_user_id}"] > a  '''
print(search_result_selector)

# with open("render_pic_response.txt", "r") as f:
#     render_pic_response = json.load(f)
#     tes = render_pic_response['post']
#     photo_id = tes['id']
#
# with open('image_id_list.txt') as f:
#     posted_img_id_array = [line.rstrip() for line in f]
#     print(len(posted_img_id_array))
#
# i = len(posted_img_id_array) - 1
# count = 0
# while count < 8:
#     print(posted_img_id_array[i])
#     i -= 1  # decrements value of i so it can run thru the array
#     count += 1
#
#
#
#
