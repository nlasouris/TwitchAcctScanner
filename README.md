# TwitchAcctScanner
Codes to monitor new accounts for potential bots and dangerous usernames

Caveat: I am not a professional coder/programmer.  I built a couple tools to be a more effective moderator on Twitch, and I'm sharing them here in case it can help anyone else.

These tools are python3 scripts that I run in command line.
NewAcctScanner.py polls the Twitch API to look through new usernames and flag ones of concern.  Please see https://dev.twitch.tv/docs/api/ to obtain your own client ID to be able to make API requests.  There is a flag in the code to enable logging all usernames to a textfile called newaccts.csv

NewAcctSpecName.py searches through newaccts.csv for names matching a specific pattern.
