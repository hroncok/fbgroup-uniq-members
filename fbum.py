import os
import requests

# required to work with Facebook Graph API
# get it from https://developers.facebook.com/docs/apps/register
# or ask @hroncok to run the script
APP_ID = os.environ['APP_ID']
APP_SECRET = os.environ['APP_SECRET']

# IDs of Facebook groups
GROUPS = [
    '201628346516017',  # facebook.com/groups/pyonieri
    '1640052339543471',  # facebook.com/groups/pyladiespraha
    '1607882249477421',  # facebook.com/groups/pyladiesBrno
    '800923800012580',  # Učíme Python
]

API = 'https://graph.facebook.com/v2.11'


def create_request(url, session):
    """
    Create a Facebook request and return the json.
    :param url: URL of Facebook group
    :param session: Facebook session
    """
    r = session.get(url)
    if r.status_code >= 400:
        print(r.json()['error']['message'])
        r.raise_for_status()
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
        group_url = f"{API}/{group}/?fields=name&access_token={token}"
        members_url = (f"{API}/{group}/?fields=members.limit(0).summary(true)"
                       f"&access_token={token}")
        name = create_request(group_url, session)['name']
        members = create_request(members_url, session)['members']
        tc = members['summary']['total_count']
        print("{name}: {tc} members.")
        total += members['summary']['total_count']

    print("Total: {} members.".format(total))

