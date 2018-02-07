import os
import requests

# required to work with Facebook Graph API
APP_ID = os.environ['APP_ID']
APP_SECRET = os.environ['APP_SECRET']

# ID of Facebook group is required!
GROUPS = ['251560641854558', '457660044251817']


def create_request(url, session):
    """
    Create a Facebook request and return the json.
    :param url: URL of Facebook group
    :param session: Facebook session
    """
    r = session.get(url)
    if r.status_code == 404:
        print('Facebook: ERROR 404 - Not Found')
        exit(5)

    if r.status_code == 401:
        print('Facebook: ERROR 401 - Bad credentials')
        exit(4)

    if r.status_code != 200:
        exit(10)

    return r.json()


def build_token(app_id=APP_ID, app_secret=APP_SECRET):
    """
    Build a Facebook access token from your APP ID and APP SECRET.
    :param app_id: Your Facebook APP ID
    :param app_secret: Your Facebook APP SECRET
    """
    access_token = app_id + '|' + app_secret
    return access_token


if __name__ == '__main__':
    total = 0
    token = build_token()
    session = requests.Session()

    for group in GROUPS:
        group_url = "https://graph.facebook.com/v2.11/{}/?access_token={}".format(group, token)
        members_url = "https://graph.facebook.com/v2.11/{}/?fields=members.limit(0).summary(true)" \
                      "&access_token={}".format(group, token)
        name = create_request(group_url, session)['name']
        members = create_request(members_url, session)['members']
        print("{}: {} members.".format(name, members['summary']['total_count']))
        total += members['summary']['total_count']

    print("Total: {} members.".format(total))

