#!/usr/local/bin/python2.7

# Credentials to access databases as the webdb user.

# Also creates a function to replace the MySQL.connect method and
# reassigns the error class, so that we reduce the number of dependencies
# on MySQLdb

import MySQLdb
import re

Error = MySQLdb.Error

def file_contents(filename):
    '''Returns contents of file as a string.'''
    file = open(filename,"r")
    contents = file.read()
    file.close()
    return contents

def read_cnf(cnf_file):
    cnf = file_contents(cnf_file)
    credentials = {}
    mapping = {'host':'host',
               'user':'user',
               'password':'passwd',
               'database':'db'}
    for key in ('host', 'user', 'password', 'database' ):
        cred_key = mapping[key]
        regex = r"\b{k}\s*=\s*[\'\"]?(\w+)[\'\"]?\b".format(k=key)
        # print 'regex',regex
        p = re.compile(regex)
        m = p.search(cnf)
        if m:
            credentials[ cred_key ] = m.group(1)
        elif key == 'host' or key == 'database':
            credentials[ cred_key ] = 'not specified in ' + cnf_file
        else:
            raise Exception('Could not find key {k} in {file}'.format(k=key,file=cnf_file))
    return credentials

# this is essentially a static variable of this package. It caches the DB
# connection, so that it can be returned quickly without setting up a new
# connection, if the user tries to connect again.  

the_database_connection = False

def connect(dsn):
    '''Returns a database connection/handle given the dsn (a dictionary)

This function saves the database connection, so if you invoke this again,
it gives you the same one, rather than making a second connection.  This
is the so-called Singleton pattern.  In a more sophisticated
implementation, the DSN would be checked to see if it has the same data as
for the cached connection.'''
    global the_database_connection
    if not the_database_connection:
        try:
            the_database_connection = MySQLdb.connect( **dsn )
            # so each modification takes effect automatically
            the_database_connection.autocommit(True)
        except MySQLdb.Error, e:
            print ("Couldn't connect to database. MySQL error %d: %s" %
                   (e.args[0], e.args[1]))
            raise
    return the_database_connection

if __name__ == '__main__':
    print 'starting test code'
    import sys
    if len(sys.argv) < 2:
        print '''Usage: {cmd} DSNfile
test dbconn by giving the name of a DSN file on the command line'''.format(cmd=sys.argv[0])
        sys.exit(1)
    dsnfile = sys.argv[1]
    module = __import__(dsnfile)
    DSN = module.DSN
    DSN['database']='wmdb'
    c = connect(DSN)
    print 'successfully connected'
    curs = c.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select user() as user, database() as db')
    row = curs.fetchone()
    print 'connected to {db} as {user}'.format(db=row['db'],user=row['user'])
    
