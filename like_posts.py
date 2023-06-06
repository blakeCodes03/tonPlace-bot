import requests


#  this function adds image ids in image_id_list.txt to an array and sends requests for like()
def like_posts():
    with open("token_value.txt", "r") as f:  # reads token value and splits
        token = f.read()
        token_value = token.split(",")
        authorization = token_value[1]


    with open('image_id_list.txt') as f:  # adds each line of image ids in the file to an array
        posted_img_id_array = [line.rstrip() for line in f]

    i = len(posted_img_id_array) - 1
    count = 0
    while count < 8:
        count += 1



        url = f"https://api.ton.place/likes/{posted_img_id_array[i]}/post/add"

        payload = {}
        files={}
        headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
          'Accept': 'application/json, text/plain, */*',
          'Accept-Language': 'en',
          'Accept-Encoding': 'gzip, deflate, br',
          'Referer': 'https://ton.place/',
          'Version': '8',
          'Timezone': '-60',
          'Origin': 'https://ton.place',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-site',
          'Authorization': authorization,
          'Connection': 'keep-alive',
          'Alt-Used': 'api.ton.place',
          'Content-Length': '0',
          'TE': 'trailers'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)
        i -= 1  # decrements value of i so it can run thru the array


# like_posts()
