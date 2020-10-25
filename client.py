#!/usr/bin/env python3.8

from stravalib.client import Client
import pickle
import time
import pprint

MY_STRAVA_CLIENT_ID, MY_STRAVA_CLIENT_SECRET = open('./client.secret').read().strip().split(',')

#auth based on: https://medium.com/analytics-vidhya/accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17

# One time authorize app:
#
# print ('Client ID and secret read from file'.format(MY_STRAVA_CLIENT_ID) )
# url = client.authorization_url(client_id=MY_STRAVA_CLIENT_ID, redirect_uri='http://127.0.0.1:5000/authorization', scope=['read_all','profile:read_all','activity:read_all'])
# print (url)
# CODE = '' #enter `code` from callback url
# access_token = client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, code=CODE)
# with open('./access_token.pickle', 'wb') as f:
#    pickle.dump(access_token, f)

client = Client()

with open('./access_token.pickle', 'rb') as f:
    access_token = pickle.load(f)

print('Latest access token read from file:')
print(access_token)

if time.time() > access_token['expires_at']:
    print('Token has expired, will refresh')
    refresh_response = client.refresh_access_token(client_id=MY_STRAVA_CLIENT_ID, client_secret=MY_STRAVA_CLIENT_SECRET, refresh_token=access_token['refresh_token'])
    access_token = refresh_response
    with open('./access_token.pickle', 'wb') as f:
        pickle.dump(refresh_response, f)
    print('Refreshed token saved to file')
    client.access_token = refresh_response['access_token']
    client.refresh_token = refresh_response['refresh_token']
    client.token_expires_at = refresh_response['expires_at']

else:
    print('Token still valid, expires at {}'
          .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))
    client.access_token = access_token['access_token']
    client.refresh_token = access_token['refresh_token']
    client.token_expires_at = access_token['expires_at']

athlete = client.get_athlete()
print("Athlete's name is {} {}, based in {}, {}"
      .format(athlete.firstname, athlete.lastname, athlete.city, athlete.country))

activities = client.get_activities(limit=20)
pprint.pprint(list(activities))

for act in (list(activities)):
    #pprint.pprint(act.highlighted_kudosers)
    kudositerator = client.get_activity_kudos(act.id)
    for kudos in kudositerator:
        print(kudos.firstname,kudos.lastname)