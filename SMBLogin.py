import sys
import argparse
import os
import smb
import socket
import time
from smb.SMBConnection import SMBConnection

def countdown(t, w):
    while t > 0:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write('Trying the next ' + w + ' in ' + timeformat + '.     \r')
        t -= 1
        time.sleep(1)

def login_check(u, p, t, d, s, o, port, timeout):
    ow = None

    if o:
        if os.path.exists(o):
            ow = True if raw_input('"' + o + '" already exists. Overwrite? [N/y]: ').lower() == 'y' else False
        else:
            ow = True

        if ow:
            of = open(o, 'w+')

    if type(u) == str:
        ul = [u]
    else:
        ul = u.readlines()

    if type(p) == str:
        pl = [p]
    else:
        pl = p.readlines()

    if type(t) == str:
        tl = [t]
    else:
        tl = t.readlines()

    tcount = len(tl)

    for targets in tl:
        targets = targets.strip()
        pcount = len(pl)

        for passwords in pl:
            passwords = passwords.strip()

            for users in ul:
                users = users.strip()

                if port == 445:
                    conn = SMBConnection(users, passwords, 'allyourbase', targets, d, is_direct_tcp=True, use_ntlm_v2=True)

                    try:
                        if conn.connect(targets, 445, timeout=timeout):
                            result = '[+] Login successful on ' + targets + ': ' + d + '\\' + users + ':' + passwords
                        else:
                            result = '[-] Login unsuccessful on ' + targets + ': ' + d + '\\' + users + ':' + passwords
                    except smb.smb_structs.ProtocolError:
                        result = '[+] Login successful on ' + targets + ', but unable to connect: ' + d + '\\' + users + ':' + passwords
                    except socket.timeout:
                        result = 'Error: timeout connecting to ' + targets
                else:
                    conn = SMBConnection(users, passwords, 'allyourbase', targets, d, is_direct_tcp=False, use_ntlm_v2=True)

                    try:
                        if conn.connect(targets, 139, timeout=timeout):
                            result = '[+] Login successful on ' + targets + ': ' + d + '\\' + users + ':' + passwords
                        else:
                            result = '[-] Login unsuccessful on ' + targets + ': ' + d + '\\' + users + ':' + passwords
                    except smb.smb_structs.ProtocolError:
                        result = '[+] Login successful on ' + targets + ', but unable to connect: ' + d + '\\' + users + ':' + passwords
                    except socket.timeout:
                        result = 'Error: timeout connecting to ' + targets

                print(result)

                if ow:
                    of.write(result + '\n')

            if pcount > 1:
                pcount -= 1
                countdown(s * 60, 'password')

        if tcount > 1:
            tcount -= 1
            countdown(s * 60, 'target')

    if ow:
        of.close()

def main(argv):
    try:
        parser = argparse.ArgumentParser(description='SMB Password Checker')
        ugroup = parser.add_mutually_exclusive_group(required=True)
        ugroup.add_argument('-u', '--user', help='Username to check (username or username file required)')
        ugroup.add_argument('-U', '--users', help='File of usernames to check (username or username file required)')
        pgroup = parser.add_mutually_exclusive_group(required=True)
        pgroup.add_argument('-p', '--password', help='Password to check (password or password file required)')
        pgroup.add_argument('-P', '--passwords', help='File of passwords to check (password or password file required)')
        tgroup = parser.add_mutually_exclusive_group(required=True)
        tgroup.add_argument('-t', '--target', help='Target to check (target or target file required)')
        tgroup.add_argument('-T', '--targets', help='File of targets to check (target or target file required)')
        parser.add_argument('-d', '--domain', default=".", help='Domain of user')
        parser.add_argument('-s', '--sleep', default=30, type=int, help='Time to wait in between checks to prevent account lockouts')
        parser.add_argument('-o', '--output', help='File to output results to')
        parser.add_argument('--port', default=445, type=int, help='Port to use for connection (445 or 139)')
        parser.add_argument('--timeout', default=5, type=int, help='Connection timeout')
        args = parser.parse_args()

        if args.user:
            u = args.user
        else:
            u = open(args.users, 'r')

        if args.password:
            p = args.password
        else:
            p = open(args.passwords, 'r')

        if args.target:
            t = args.target
        else:
            t = open(args.targets, 'r')

        login_check(u, p, t, args.domain, args.sleep, args.output, args.port, args.timeout)
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main(sys.argv)
