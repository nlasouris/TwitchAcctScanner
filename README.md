# TwitchAcctScanner
Codes to monitor new accounts for potential bots and dangerous usernames

Caveat: I am not a professional coder/programmer.  I built a couple tools to be a more effective moderator on Twitch, and I'm sharing them here in case it can help anyone else.

These tools are python3 scripts that I run in command line.
NewAcctScanner.py polls the Twitch API to look through new usernames and flag ones of concern.  Please see https://dev.twitch.tv/docs/api/ to obtain your own client ID to be able to make API requests.  There is a flag in the code to enable logging all usernames to a textfile called newaccts.csv.  Names matching terms included as a comma-separated list in substrings.txt are flagged in command line output.  This file is checked on every loop so terms can be added quickly without restarting the program.

NewAcctSpecName.py searches through newaccts.csv for names matching a specific pattern.

Right now this is basically a logger/flagger, so I can find accounts to report but otherwise take no action.  I'm hoping that those who need to can integrate this with their own chatbots etc., especially if they have their own Python IRC interfaces to Twitch chat, that will automate banning and blocking accounts that have dangerous (e.g. doxxing) information in the names.
