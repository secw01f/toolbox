#!/usr/bin/env python3

import argparse
import logging
import sys
import os
import importlib
import subprocess
import shutil
import readline
import sqlite3

def interactive():
    while True:
        prompt = input(('(%s)>>> ' % (os.getlogin())))
        cmd = prompt.rsplit()
        if not cmd:
            pass
        elif cmd[0] == 'help':
            print('help      Prints this help message')
            print('cmd       Runs the provided command line command')
            print('run       Runs the provided module and its provided arguments')
            print('list      Lists available modules')
            print('import    Imports defined module [Ex. import example.py]')
            print('key       Adds a key for a module')
            print('clear     Clears the command line')
            print('cd        Change current directory')
            print('ls        List current directory contents')
            print('exit      Exits the toolbox')
        elif cmd[0] == 'cmd':
            cmd.remove('cmd')
            try:
                subprocess.call(cmd)
            except:
                pass
        elif cmd[0] == 'run':
            cmd.remove('run')
            module = cmd[0]
            cmd.remove(module)
            try:
                importlib.import_module(str('modules.' + module)).module(cmd)
            except:
                pass
        elif cmd[0] == 'list':
            conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
            cur = conn.cursor()
            cur.execute('SELECT * FROM config;')
            config = str(cur.fetchone()[0])
            if config == 'offensive':
                cur.execute('SELECT * FROM modules WHERE category="recon";')
                recon = cur.fetchall()

                print('<=====[ RECONNAISSANCE ]=====>\n')
                for row in recon:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="listener";')
                listener = cur.fetchall()

                print('\n\n<=====[ LISTENERS ]=====>\n')
                for row in listener:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="exploit";')
                exploit = cur.fetchall()

                print('\n\n<=====[ EXPLOITS ]=====>\n')
                for row in exploit:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="post_exploit";')
                post_exploit = cur.fetchall()

                print('\n\n<=====[ POST EXPLOITATION ]=====>\n')
                for row in post_exploit:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="misc";')
                misc = cur.fetchall()

                print('\n\n<=====[ MISCELLANEOUS ]=====>\n')
                for row in misc:
                    print(str(row[1] + '     ' + row[3]))
            elif config == 'defensive':
                cur.execute('SELECT * FROM modules WHERE category="sec_engineering";')
                sec_eng = cur.fetchall()

                print('<=====[ SECURITY ENGINEERING ]=====>\n')
                for row in sec_eng:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="app_security";')
                app_sec = cur.fetchall()

                print('\n\n<=====[ APPLICATION SECURITY ]=====>\n')
                for row in app_sec:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="incident_response";')
                incident_response = cur.fetchall()

                print('\n\n<=====[ INCIDENT RESPONSE ]=====>\n')
                for row in incident_response:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="vuln_management";')
                vuln_management = cur.fetchall()

                print('\n\n<=====[ VULNERABILITY MANAGEMENT ]=====>\n')
                for row in vuln_management:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="misc";')
                misc = cur.fetchall()

                print('\n\n<=====[ MISCELLANEOUS ]=====>\n')
                for row in misc:
                    print(str(row[1] + '     ' + row[3]))
            cur.close()
            conn.close()
            
        elif cmd[0] == 'import':
            dir = os.path.dirname(os.path.realpath(__file__))
            try:
                shutil.copy(cmd[1], str(dir + '/modules'))
                conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                cur = conn.cursor()
                module = str(cmd[1].split('.')[0])
                details = importlib.import_module(str('modules.' + module)).details()
                cur.execute('INSERT INTO modules(name, category, description, path, key) VALUES(?,?,?,?,?);', (details['name'], details['category'], details['description'], details['path'], details['key']))
                conn.commit()
                cur.close()
                conn.close()
                print('[ + ] Module import successful')
                if details['key'] == True:
                    print('This module requires a key')
                else:
                    pass
            except:
                print('[ ! ] Import Failed')
                pass
        elif cmd[0] == 'key':
            if not cmd[1]:
                print('[ ! ] An action is required')
                print('key add')
                print('key delete')
                print('key list')
                continue
            elif cmd[1] == 'add':  
                module = input('Module Name [Required]: ')
                if not module:
                    print('[ ! ] Module name is required')
                    continue
                user = input('User Name [Optional]: ')
                key = input('Key Value [Required]: ')
                if not key:
                    print('[ ! ] Key value is required')
                    continue
                try:
                    conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                    cur = conn.cursor()
                    cur.execute('INSERT INTO keys(module, user, key) VALUES(?,?,?);', (module, user, key))
                    conn.commit()
                    cur.close()
                    conn.close()
                    print('[ + ] Key added successfully')
                except:
                    print('[ ! ] Key addition failed')
                    pass
            elif cmd[1] == 'delete':
                module = input('Module Name [Required]: ')
                if not module:
                    print('[ ! ] Module Name is required')
                    continue
                else:
                    pass
                try:
                    conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                    cur = conn.cursor()
                    cur.execute('DELETE FROM keys WHERE module=?;', (module,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    print('[ + ] Key deleted successfully')
                except:
                    print('[ ! ] Key deletion failed')
                    pass
            elif cmd[1] == 'list':
                conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                cur = conn.cursor()
                cur.execute('SELECT * FROM keys;')
                keys = cur.fetchall()
                print('<=====[ KEYS ]=====>\n')
                for row in keys:
                    print(str(row[1]))
                cur.close()
                conn.close()
        elif cmd[0] == 'clear':
            subprocess.call('clear')
        elif cmd[0] == 'cd':
            os.chdir(cmd[1])
        elif cmd[0] == 'ls':
            subprocess.call(cmd)
        elif cmd[0] == 'exit':
            sys.exit()

def interactive_logged():
    logging.basicConfig(filename=str('%s/.toolbox/toolbox.log' % (os.path.expanduser('~'))), format="%(asctime)s : %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p", level=logging.INFO)
    logging.info('Session Started')
    while True:
        prompt = input(('(%s)>>> ' % (os.getlogin())))
        cmd = prompt.rsplit()
        if not cmd:
            pass
        elif cmd[0] == 'help':
            print('help      Prints this help message')
            print('cmd       Runs the provided command line command')
            print('run       Runs the provided module and its provided arguments')
            print('list      Lists available modules')
            print('import    Imports defined module [Ex. import example.py]')
            print('clear     Clears the command line')
            print('cd        Change current directory')
            print('ls        List current directory contents')
            print('exit      Exits the toolbox')
        elif cmd[0] == 'cmd':
            cmd.remove('cmd')
            try:
                subprocess.call(cmd)
                logging.info('cmd: %s - Success', ' '.join(cmd))
            except:
                logging.info('cmd: %s - Failed', ' '.join(cmd))
                pass
        elif cmd[0] == 'run':
            cmd.remove('run')
            module = cmd[0]
            cmd.remove(module)
            try:
                importlib.import_module(str('modules.' + module)).module(cmd)
                logging.info('run: %s - Success', ' '.join(cmd))
            except:
                logging.info('run: %s - Failed', ' '.join(cmd))
                pass
        elif cmd[0] == 'list':
            conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
            cur = conn.cursor()
            cur.execute('SELECT * FROM config;')
            config = str(cur.fetchone()[0])
            if config == 'offensive':
                cur.execute('SELECT * FROM modules WHERE category="recon";')
                recon = cur.fetchall()

                print('<=====[ RECONNAISSANCE ]=====>\n')
                for row in recon:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="listener";')
                listener = cur.fetchall()

                print('\n\n<=====[ LISTENERS ]=====>\n')
                for row in listener:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="exploit";')
                exploit = cur.fetchall()

                print('\n\n<=====[ EXPLOITS ]=====>\n')
                for row in exploit:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="post_exploit";')
                post_exploit = cur.fetchall()

                print('\n\n<=====[ POST EXPLOITATION ]=====>\n')
                for row in post_exploit:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="misc";')
                misc = cur.fetchall()

                print('\n\n<=====[ MISCELLANEOUS ]=====>\n')
                for row in misc:
                    print(str(row[1] + '     ' + row[3]))
            elif config == 'defensive':
                cur.execute('SELECT * FROM modules WHERE category="sec_engineering";')
                sec_eng = cur.fetchall()

                print('<=====[ SECURITY ENGINEERING ]=====>\n')
                for row in sec_eng:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="app_security";')
                app_sec = cur.fetchall()

                print('\n\n<=====[ APPLICATION SECURITY ]=====>\n')
                for row in app_sec:
                    print(str(row[1] + '     ' + row[3]))

                cur.execute('SELECT * FROM modules WHERE category="incident_response";')
                incident_response = cur.fetchall()

                print('\n\n<=====[ INCIDENT RESPONSE ]=====>\n')
                for row in incident_response:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="vuln_management";')
                vuln_management = cur.fetchall()

                print('\n\n<=====[ VULNERABILITY MANAGEMENT ]=====>\n')
                for row in vuln_management:
                    print(str(row[1] + '     ' + row[3]))
            
                cur.execute('SELECT * FROM modules WHERE category="misc";')
                misc = cur.fetchall()

                print('\n\n<=====[ MISCELLANEOUS ]=====>\n')
                for row in misc:
                    print(str(row[1] + '     ' + row[3]))
            
        elif cmd[0] == 'import':
            dir = os.path.dirname(os.path.realpath(__file__))
            try:
                shutil.copy(cmd[1], str(dir + '/modules'))
                conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                cur = conn.cursor()
                module = str(cmd[1].split('.')[0])
                details = importlib.import_module(str('modules.' + module)).details()
                cur.execute('INSERT INTO modules(name, category, description, path) VALUES(?,?,?,?,?);', (details['name'], details['category'], details['description'], details['path'], details['key']))
                conn.commit()
                cur.close()
                conn.close()
                print('[ + ] Module import successful')
                logging.info('import: %s - Success', ' '.join(cmd))
            except:
                print('[ ! ] Import Failed')
                logging.info('import: %s - Failed', ' '.join(cmd))
                pass
        elif cmd[0] == 'key':
            if not cmd[1]:
                print('[ ! ] An action is required')
                print('key add')
                print('key delete')
                print('key list')
                continue
            elif cmd[1] == 'add':  
                module = input('Module Name [Required]: ')
                if not module:
                    print('[ ! ] Module name is required')
                    continue
                user = input('User Name [Optional]: ')
                key = input('Key Value [Required]: ')
                if not key:
                    print('[ ! ] Key value is required')
                    continue
                try:
                    conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                    cur = conn.cursor()
                    cur.execute('INSERT INTO keys(module, user, key) VALUES(?,?,?);', (module, user, key))
                    conn.commit()
                    cur.close()
                    conn.close()
                    print('[ + ] Key added successfully')
                    logging.info('key: %s - Success', ' '.join(cmd))
                except:
                    print('[ ! ] Key addition failed')
                    logging.info('key: %s - Failed', ' '.join(cmd))
                    pass
            elif cmd[1] == 'delete':
                module = input('Key Name [Required]: ')
                if not module:
                    print('[ ! ] Key Name is required')
                    continue
                else:
                    pass
                try:
                    conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                    cur = conn.cursor()
                    cur.execute('DELETE FROM keys WHERE module=?;', (module,))
                    conn.commit()
                    cur.close()
                    conn.close()
                    print('[ + ] Key deleted successfully')
                    logging.info('key: %s - Success', ' '.join(cmd))
                except:
                    print('[ ! ] Key deletion failed')
                    logging.info('key: %s - Failed', ' '.join(cmd))
                    pass
            elif cmd[1] == 'list':
                conn = sqlite3.connect(r'%s/.toolbox/toolbox.db' % (os.path.expanduser('~')))
                cur = conn.cursor()
                cur.execute('SELECT * FROM keys;')
                keys = cur.fetchall()
                print('<=====[ KEYS ]=====>\n')
                for row in keys:
                    print(str(row[1]))
                cur.close()
                conn.close()
        elif cmd[0] == 'clear':
            subprocess.call('clear')
        elif cmd[0] == 'cd':
            try:
                os.chdir(cmd[1])
                logging.info('cd: %s - Success', ' '.join(cmd))
            except:
                logging.info('cd: %s - Failed', ' '.join(cmd))
        elif cmd[0] == 'ls':
            subprocess.call(cmd)
            logging.info('ls: %s', ' '.join(cmd))
        elif cmd[0] == 'exit':
            logging.info('Session Ended')
            sys.exit()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(add_help=True)
    argparser.add_argument('-l', '--log', help='Enables logging of the session', action='store_true')
    argparser.add_argument('-L', '--rlog', help='Prints the content of the toolbox log file', action='store_true')
    args = argparser.parse_args()
    sys.dont_write_bytecode = True
    if args.rlog == True:
        with open(str('%s/.toolbox/toolbox.log' % (os.path.expanduser('~'))), 'r') as logfile:
            output = logfile.read()
            print(output)
            logfile.close()
        sys.exit()
    if args.log == False:
        print('Welcome to Toolbox!\n')
        interactive()
    else:
        print('Welcome to Toolbox! - Logging Enabled\n')
        interactive_logged()
