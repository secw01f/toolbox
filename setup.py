import sqlite3
from sqlite3 import Error
import os
import sys

os.mkdir((os.path.expanduser('~') + '/.toolbox'))
dir = str(os.path.expanduser('~') + '/.toolbox')
os.system(f'sudo ln -s {os.getcwd()}/toolbox.py /usr/local/bin/toolbox')
os.chmod('toolbox.py', 0o774)

if sys.argv[1] == 'offensive':
    try:
        conn = sqlite3.connect(r'%s/toolbox.db' % (dir))
        cur = conn.cursor()
        cur.execute('CREATE TABLE config (config TEXT PRIMARY KEY NOT NULL);')
        conn.commit()
        cur.execute('INSERT INTO config(config) VALUES("offensive");')
        conn.commit()
        cur.execute('CREATE TABLE modules (id INTEGER PRIMARY KEY, name varchar(50) NOT NULL, category TEXT NOT NULL CHECK(category = "recon" or category = "listener" or category = "exploit" or category = "post_exploit" or category = "misc"), description varchar(200), path varchar(100) NOT NULL, key BOOLEAN NOT NULL);')
        conn.commit()
        cur.execute('CREATE TABLE keys (id INTEGER PRIMARY KEY, module varchar(50) NOT NULL, user varchar(50), key varchar(100) NOT NULL);')
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        sys.exit()
elif sys.argv[1] == 'defensive':
    try:
        conn = sqlite3.connect(r'%s/toolbox.db' % (dir))
        cur = conn.cursor()
        cur.execute('CREATE TABLE config (config TEXT PRIMARY KEY NOT NULL);')
        conn.commit()
        cur.execute('INSERT INTO config(config) VALUES("defensive");')
        conn.commit()
        cur.execute('CREATE TABLE modules (id INTEGER PRIMARY KEY, name varchar(50) NOT NULL, category TEXT NOT NULL CHECK(category = "sec_engineering" or category = "app_security" or category = "incident_response" or category = "vuln_management" or category = "misc"), description varchar(200), path varchar(100) NOT NULL, key BOOLEAN NOT NULL);')
        conn.commit()
        cur.execute('CREATE TABLE keys (id INTEGER PRIMARY KEY, module varchar(50) NOT NULL, user varchar(50), key varchar(100) NOT NULL);')
        conn.commit()
        cur.close()
        conn.close()
    except Error as e:
        print(e)
        sys.exit()
