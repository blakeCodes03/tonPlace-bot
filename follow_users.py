import requests
import json
import random

#  this function follows different users with user_id gotten from accounts.json file
def follow_users():

    with open("token_value.txt", "r") as f:  # reads token value and splits
        token = f.read()
        token_value = token.split(",")
        authorization = token_value[1]

    i = 0
    while i < 8:

        f = open('accounts.json', )
        users = json.load(f)  # loads accounts.json file
        randomly_selected_user = random.choice(users)  # selects random account frpm the file
        selected_user = randomly_selected_user["userID"]  # selects userID of selected user
        user_id = selected_user.split("d")[1]  # splits userID e.g(from:"/id312605"  into:['/id', '312605']) and selects the interger






        url = f"https://api.ton.place/follow/{user_id}/add?recommended_authors=0"

        payload = {}
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

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        i += 1


# follow_users()