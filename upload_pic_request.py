import requests
import random
import os


def upload_pic():
    with open("token_value.txt", "r") as f:
        token = f.read()
        token_value = token.split(",")
        authorization = token_value[1]

    url = "https://api.ton.place/photos/upload"

    payload = {'album_id': '-3'}

    dir_image = "images/"
    file = os.listdir(dir_image)
    chosen_image = random.choice(file)
    with open(os.path.join(dir_image,chosen_image), 'rb') as file:
        files = {'file': (chosen_image, file, 'image/jpeg')}
        # files = [
        #     ('file', open(chosen_image))
        # ]
        # files=[
        #   ('file',('ab3b514b895b8786a5e0fa7826ad205d.jpg',open('/C:/Users/Diggz/Pictures/pictures/pintrest/ab3b514b895b8786a5e0fa7826ad205d.jpg','rb'),'image/jpeg'))
        # ]
        headers = {
          'authority': 'api.ton.place',
          'accept': '*/*',
          'accept-language': 'en-US,en;q=0.9',
          'access-control-request-headers': 'authorization,timezone,version',
          'access-control-request-method': 'POST',
          'origin': 'https://ton.place',
          'referer': 'https://ton.place/',
          'sec-fetch-dest': 'empty',
          'sec-fetch-mode': 'cors',
          'sec-fetch-site': 'same-site',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
          'method': 'POST',
          'authorization': authorization
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    with open("upload_pic_response.txt", "w") as f:
        f.write(f"{response.text}")


upload_pic()