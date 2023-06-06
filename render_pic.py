import requests
import json
from follow_users import follow_users
from posted_img_id import image_id_lists
from like_posts import like_posts


def render_new_pic():

    with open("token_value.txt", "r") as f:  # reads token value and splits
        token = f.read()
        token_value = token.split(",")
        authorization = token_value[1]
        owner_id = token_value[0]

    with open("upload_pic_response.txt", "r") as f:  # reads json response and obtains photo_id
        photo_id_response = json.load(f)
        photo_id = photo_id_response['photo_id']


    url = "https://api.ton.place/posts/new"

    payload = json.dumps({
      "ownerId": int(owner_id),
      "text": "",
      "type": 1,
      "parentId": 0,
      "attachments": [
        {
          "type": "photo",
          "photo": {
            "photoId": int(photo_id)
          }
        }
      ],
      "timer": 0,
      "skipBotPost": True
    })
    headers = {
      'authority': 'api.ton.place',
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'en',
      'authorization': authorization,
      'content-type': 'application/json',
      'origin': 'https://ton.place',
      'referer': 'https://ton.place/',
      'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'timezone': '-60',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    if response.ok:
        with open("render_pic_response.txt", "w") as f:
            f.write(response.text)
        follow_users()
        image_id_lists()
        like_posts()


render_new_pic()
