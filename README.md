# SMBLogin

This tool is used to check passwords against an SMB server with an added delay to prevent account lockout.

usage: SMBLogin.py [-h] (-u USER | -U USERS) (-p PASSWORD | -P PASSWORDS)
                   (-t TARGET | -T TARGETS) [-d DOMAIN] [-s SLEEP] [-o OUTPUT]
                   [--port PORT] [--timeout TIMEOUT]

SMB Password Checker

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Username to check (username or username file required)
  -U USERS, --users USERS
                        File of usernames to check (username or username file
                        required)
  -p PASSWORD, --password PASSWORD
                        Password to check (password or password file required)
  -P PASSWORDS, --passwords PASSWORDS
                        File of passwords to check (password or password file
                        required)
  -t TARGET, --target TARGET
                        Target to check (target or target file required)
  -T TARGETS, --targets TARGETS
                        File of targets to check (target or target file
                        required)
  -d DOMAIN, --domain DOMAIN
                        Domain of user
  -s SLEEP, --sleep SLEEP
                        Time to wait in between checks to prevent account
                        lockouts
  -o OUTPUT, --output OUTPUT
                        File to output results to
  --port PORT           Port to use for connection (445 or 139)
  --timeout TIMEOUT     Connection timeout
