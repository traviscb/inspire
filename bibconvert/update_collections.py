"""
Input:   Dumps collection configuration to SQL that can be reloaded.
Must use invenio web collection admin websearch to modify configuration


-f: filename - defaults to coll.conf
-h: this help
-u: update from file
-d: dump to file <- default


    the numrecs and records in the dump of collections are meaningless, but will be
    fixed upon rerunning webcoll.

"""

import sys, getopt, os
from invenio.config import CFG_LOGDIR, CFG_PATH_MYSQL, CFG_DATABASE_HOST, \
     CFG_DATABASE_USER, CFG_DATABASE_PASS, CFG_DATABASE_NAME
from invenio.shellutils import run_shell_command, escape_shell_arg
from invenio.dbquery import run_sql
from ConfigParser import RawConfigParser

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hfdu",["help","file","dump","update"])
    except getopt.GetoptError, err:
        print str(err)
        print __doc__
        sys.exit(2)
    filename = "coll.conf"
    dirname = "."
    drop = False
    dump = True
    update = False
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit()
        if o in ("-f", "--file"):
            filename = a
        if o in ('-u', "--update"):
            update = True
            dump = False
        if o in ("-d", "--dump"):
            dump = True



    if (update and drop):
        run_sql("DROP TABLE IF EXISTS tag, field, field_tag")


    if (dump):
        print("... writing %s" % dirname + os.sep + filename)
        dump_collections(dirname + os.sep + filename)
    elif (update):
        print("... updating from %s" % dirname + os.sep + filename)
        fill_collections(dirname + os.sep + filename)


def dump_collections(filename):
    """ Dumps the current values of the collection settings from the
    invenio instance into a file of mysql commands  does not use mysqldump
    -T  so that it can control the columns used

    the numrecs and record are not stored, but will be
    fixed upon rerunning webcoll.

    """

    # some tables need only certain columns, all others get all columns
    SPECIAL_COLUMNS = {"collection": "id,name,dbquery,restricted"}


    f = open (filename, 'w')
    
    tables = run_sql("SHOW TABLES like 'collection%'")
    for (table,) in tables:

        if table in SPECIAL_COLUMNS:
            columns = SPECIAL_COLUMNS[table]
            insert_columns = "(" + SPECIAL_COLUMNS[table] + ")"
        else:
            columns = "*"
            insert_columns = ""
    
        cmd = "SELECT " + columns + " from " + table
        rows = run_sql(cmd)
        f.write ("TRUNCATE "+table +"\n")
        for row in rows:
            f.write("INSERT INTO "+ table + insert_columns + " VALUES ("+ \
                  ','.join(["\'"+ str(a).replace("\'","\\\'") +"\'" for a in row])+")\n")
            
        


def fill_collections(filename):

    """ uses file as a series of SQL commands to laod the collections
    information back to the instance """



    f = open (filename, 'r')
    
    for line in f:
        print line
        result = run_sql(line)
        print result



if __name__ == "__main__":
    main()
