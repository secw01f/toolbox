import sqlite3
from sqlite3 import Error
import os
import sys

os.mkdir((os.path.expanduser('~') + '/.toolbox'))
dir = str(os.path.expanduser('~') + '/.toolbox')

try:
    conn = sqlite3.connect(r'%s/modules.db' % (dir))
    cur = conn.cursor()
    cur.execute('CREATE TABLE modules (id INTEGER PRIMARY KEY, name varchar(50) NOT NULL, category TEXT NOT NULL CHECK(category = "recon" or category = "listener" or category = "exploit" or category = "post_exploit" or category = "misc"), description varchar(200), path varchar(100) NOT NULL);')
    conn.commit()
    cur.close()
    conn.close()
except Error as e:
    print(e)
    sys.exit()
