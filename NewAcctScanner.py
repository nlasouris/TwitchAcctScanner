#! /usr/bin/env python3

import requests
import time
import datetime
import TwitchClientAuth
# clientid = '<get this from Twitch dev site>'
clientid = TwitchClientAuth.clientid

start_id = 719922698 # Initial ID to start scanning - need to set to auto-update based on last entry in newaccts.csv
logall = True
logflagged = True

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
#    consolemsg('Token expires at '+expireDatetime.strftime('%Y-%m-%dT%H:%M:%S')) # Print token information for debugging
    return token
  else:
    return 'null'

def compstr(string1, string2): # THIS NEEDS TO BE BETTER - for now just compare corresponding letters between adjacents
  # To do: implement queue with selectable size to compare against more than just the prior single account
  common = 0
  minlen = min(len(string1),len(string2))
  for x,y in zip(string1[0:minlen],string2[0:minlen]):
    if x == y:
      common += 1
  return common

token = getAccessToken()
getheader = {'client-id': TwitchClientAuth.clientid, 'Authorization': 'Bearer ' + token}

while True:
  try:
    with open('substrings.txt','r') as substringfile:
      substrings = substringfile.readline().split(', ') # Update list of flagged substrings on every loop to allow changes on the fly
    print(start_id) # Print first ID of the batch
    getpayload = {'id': [str(i) for i in range(start_id,start_id+100,1)]} # Make a list of numbers, convert to string for API call
    r1 = requests.get('https://api.twitch.tv/helix/users', headers=getheader,   params=getpayload)
    # print('Rate limit remaining: ' + r1.headers['Ratelimit-Remaining']) # Just checking that I don't overload API rate limit
    users = sorted(r1.json()['data'], key=lambda i:i['id'])             # Sort response by user ID
    user = users[0]                                                     # Special case for the first in list (no comparison)
    if logall:
      with open('newaccts.csv','a') as allfile:
        allfile.write('{1},{0},{2}\n'.format(user['id'],user['display_name'],user['created_at'])) # Record in master list
        allfile.flush()
    for substring in substrings:
      if substring in user['display_name']:
        print('{0},{1},{2}\n'.format(user['id'],user['display_name'],user['created_at']))
    prevuser = user['display_name']
    for user in users[1:]:
      if logall:
        with open('newaccts.csv','a') as allfile:
          allfile.write('{1},{0},{2}\n'.format(user['id'],user['display_name'],user['created_at'])) # Record in master list
          allfile.flush()
      for substring in substrings:
        if substring in user['display_name']:
          print('{0},{1},{2}\n'.format(user['id'],user['display_name'],user['created_at']))
      common = compstr(prevuser,user['display_name'])
      if common > 5: # Flag any username that shares more than five common letters with the previous
        if logflagged:
          with open('newbotaccts.csv', 'a') as botfile:
            botfile.write('{0},{1},{2},{3}\n'.format(user['id'],user['display_name'],user['created_at'],prevuser)) # If flagged, write to shortlist
            botfile.flush()
        consolemsg('{0},{1},{2},{3}\n'.format(user['id'],user['display_name'],user['created_at'],prevuser))
      prevuser = user['display_name']
    dt = datetime.datetime.utcnow()-datetime.datetime.strptime(users[-1]['created_at'],'%Y-%m-%dT%H:%M:%SZ') # Check how old latest account is
    consolemsg('Latency from last account scanned: ' + str(dt))
    if dt < datetime.timedelta(minutes=1): # If approaching the end of list (processing too quickly) sleep for a longer time
      time.sleep(30)
    elif dt > datetime.timedelta(minutes=3): # If pretty far from end of list, speed up processing
      time.sleep(1)
    else:
      time.sleep(15) # Standard delay of 15 seconds to balance roughly with account creation rate

    start_id = int(users[-1]['id'])+1
  except Exception as e:
    consolemsg('Failed on lookup')
    print(e)
    break

