## Scan for specific name pattern through all history

import requests
import time
import datetime
import TwitchClientAuth
import re

# clientid = '<get this from Twitch dev site>'
clientid = TwitchClientAuth.clientid

subname = 'manofsteel'

def consolemsg(str):
  print('[' + datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '-API] ' + str)

def getAccessToken():
  oauthpostdata = {'client_id':     TwitchClientAuth.clientid,
                   'client_secret': TwitchClientAuth.clientsecret,
                   'grant_type':   'client_credentials'}
  r1 = requests.post('https://id.twitch.tv/oauth2/token', data=oauthpostdata)
  if r1.status_code == 200:
    token = r1.json()['access_token']
    expireDatetime = datetime.datetime.now() + datetime.timedelta(seconds=r1.json()['expires_in'])
#    consolemsg('Token: '+token)
#    consolemsg('Token expires at '+expireDatetime.strftime('%Y-%m-%dT%H:%M:%S'))
    return token
  else:
    return 'null'

token = getAccessToken()
getheader = {'client-id': TwitchClientAuth.clientid, 'Authorization': 'Bearer ' + token}

start_id = 0 # Or other loop index depending on pattern being searched

with open('manofsteel-20210825-0700-all.csv', 'w') as botfile:
  while start_id < 3500: # Or other end condition
    try:
      print(start_id)
      # Here set up a query for names matching substring + number
      getpayload = {'login': ['manofsteel'+str(i) for i in range(start_id,start_id+100,1)]}
      r1 = requests.get('https://api.twitch.tv/helix/users', headers=getheader, params=getpayload)
      print('Rate limit remaining: ' + r1.headers['Ratelimit-Remaining'])
      resp = r1.json()
      if 'data' in resp:
        users = sorted(r1.json()['data'], key=lambda i:i['id'])
        for user in users:
          botfile.write('{1},{0},{2}\n'.format(user['id'],user['display_name'],user['created_at']))
      start_id += 100
    except:
      print('failed on lookup')
      break
