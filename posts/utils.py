import requests

def check_if_userid_exists(request):
    responseUsers = requests.get('https://jsonplaceholder.typicode.com/users')
    for user in responseUsers.json():
        userid = user['id']
        if int(userid) == int(request.data['userid']):
            return True
    return False

def check_if_post_exists(postid):
    responsePosts = requests.get('https://jsonplaceholder.typicode.com/posts/' + str(postid))
    if responsePosts.status_code == 404:
        return False
    return responsePosts.json()