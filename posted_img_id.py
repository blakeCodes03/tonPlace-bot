import json


def image_id_lists():
    with open("render_pic_response.txt", "r") as f:  # opens file and reads json response
        render_pic_response = json.load(f)
        tes = render_pic_response['post']
        photo_id = tes['id']

    with open("image_id_list.txt", "a") as f:  # opens file and appends latest-posted image id to a new line in the file
        f.write(f"{photo_id} \n")


# image_id_lists()

