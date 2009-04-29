"""
Input: simple text table of field names and MARC disgnations for upload
into the tags table

-f: filename
-F: Force updates, regardless of existing tag names
-h: this help

"""

import sys, getopt
from invenio.dbquery import run_sql
from ConfigParser import RawConfigParser

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "DFhdf:",["help","file","Force","dump", "Drop"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    filename = None
    force = False
    dump = False
    drop = False
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit()
        if o in ("-f", "--file"):
            filename = a
        if o in ("-F", "--Force"):
            force = True
        if o in ("-d", "--dump"):
            dump = True
        if o in ('-D', "--Drop"):
            drop = True

    if (filename == None):
        print "Need a filename"
        print __doc__
        sys.exit(2)

    if (drop):
        run_sql("DROP TABLE IF EXISTS tag, field, field_tag")

    if (dump):
        dump_config_file(filename)
    else:

        fill_tag_table(get_dict(filename,"tagnames"))
        fill_field_table(get_dict(filename,"fieldnames"))
        fill_fieldtag_table(get_dict(filename,"fieldtags"))


def fill_tag_table(translations):
    """ This function takes a list of tag, name pairs """

    for tag, name in translations:
    #first check for dupes, then resolve, then finally INSERT...

        try:
            res = run_sql("SELECT id,name FROM tag WHERE value=%s", (tag,))

            if(len(res) == 0):
                new_ID = run_sql("""INSERT INTO tag (value,name) VALUES (%s,%s) """, (tag, name))              
                print "Added %s to tag table, called %s, id is %s" % (tag, name, new_ID)
            elif (len(res) == 1):
                if len(res[0]) == 2:
                    if res[0][1] == name:
                        print "No update needed for %s (AKA:%s)" % (tag,name)
                    else:
                        print "Changing existing name of %s:  %s ---> %s"  % (tag, res[0][1], name)
                        run_sql ("UPDATE tag SET name = %s WHERE id = %s and value =%s" , (name, res[0][0], tag))
                else:    
                    run_sql ("UPDATE tag SET name = %s WHERE id = %s and value =%s" , (name, res[0][0], tag))
            else:
                if force:
                    run_sql ("UPDATE tag SET name = %s WHERE id = %s and value =%s" , (name, res[0][0], tag))
                else:    
                    raise StandardError("Multiple records matching tag %s" % (tag)) 
        except StandardError, e:
            print "Error in sql for %s: %s \n Not added" % (tag,e)
            continue


def fill_field_table(fields):
    """  takes a list of logical field, name pairs """

    for name,code in fields:

        try:
            res = run_sql("SELECT id,name FROM field WHERE code=%s", (code,))
            if(len(res) == 0):
                new_ID = run_sql("""INSERT INTO field (name, code) VALUES (%s,%s) """, (name, code))              
                print "Added %s to field table, called %s, id is %s" %        (code, name, new_ID)
            elif (len(res) == 1):
                if len(res[0]) == 2:
                    if res[0][1] == name:
                        print "No update needed for %s" % (name)
                    else:
                        print "Changing existing name of %s:  %s ---> %s"  % (code, res[0][1], name)
                        run_sql ("UPDATE field SET name = %s WHERE id = %s and code =%s" , (name, res[0][0], code))
                else:    
                    run_sql ("UPDATE field SET name = %s WHERE id = %s and code =%s" , (name, res[0][0], code))
            else:
                # Found multiple values 
                if force:
                    run_sql ("UPDATE field SET name = %s WHERE id = %s and code =%s" , (name, res[0][0], code))
                else:    
                    raise StandardError("Multiple records matching code %s" % (code)) 
        except StandardError, e:
            print "Error in sql for %s: %s \n Not added" % (code,e)
            continue



def fill_fieldtag_table(pairs):
    """  takes a list of logical field, name pairs """

    for field,tag_name_score in pairs:
        if tag_name_score.count(':') == 1 :
            (tag_name, score) = tag_name_score.split(':')
        elif tag_name_score.count(':') == 0 :
            tag_name = tag_name_score
            score = 10
        else:
            raise StandardError("improper format for tag_name:score :  %s" % (tag_name_score)) 
        try:
            tag_ids = run_sql("SELECT id FROM tag WHERE name=%s", (tag_name,))
            if(len(tag_ids) == 0):
                raise StandardError("No tag with name=%s" % tag_name)
            field_ids = run_sql("SELECT id FROM field WHERE name=%s", (field,))
            if(len(field_ids) == 0):
                raise StandardError("No field with name=%s" % field)
            for tag_id in tag_ids:
                for field_id in field_ids:
                    field_id = field_id[0]
                    tag_id = tag_id[0]
                    res = run_sql("SELECT score FROM field_tag WHERE id_field=%s and id_tag=%s", (field_id,tag_id))
                    if (len(res) == 1):
                        print "No update needed for %s <=> %s (keeping score:%d)" % (field,tag_name,res[0][0])
                    elif (len(res) == 0):
                        run_sql("""INSERT INTO field_tag (id_field,id_tag,score) VALUES (%s,%s,%s) """, (field_id,tag_id,score))              
                        print "Added to field_tag table %s <=> %s" %   (field, tag_name)
                    else:    
                        raise StandardError("Multiple field_tag rows relating  %s <=>  %s" % (field_id,tag_id)) 
        except StandardError, e:
            print "Error in sql: %s \n Not added" % (e)
            continue





def get_dict(filename, section):
    """ reads a list of pairs from file, using ConfigParser
    """
    conf = RawConfigParser()
    conf.optionxform = str
    conf.read(filename)
    return conf.items(section)




def dump_config_file(filename):
    """ dumps existing configuration to a flatfile  currently doesn't sort, due to ConfigParser not using ordered dict to store before writing
    """
#    conf = RawConfigParser()
    conf = open(filename,'w')
    dump_fieldtags(conf)
    dump_fieldnames(conf)
    dump_tagnames(conf)

    
 #   conf.write(f)
    conf.close



def dump_fieldtags(conf):
    conf.write("\n[fieldtags]\n") 
#    conf.add_section("fieldtags")
    res = run_sql("SELECT field.name,tag.name,field_tag.score FROM field,field_tag, tag WHERE field_tag.id_field = field.id AND field_tag.id_tag = tag.id ORDER BY field.name asc")
    [conf.write("%s = %s:%d\n" % (name, tag, score)) for (name,tag,score) in res]
#        conf.set('fieldtags',row[0],"%s:%d" % (row[1],row[2]))
 

def dump_fieldnames(conf):
    conf.write("\n[fieldnames]\n") 
 #   conf.add_section("fieldnames")
    res = run_sql("SELECT name,code FROM field ORDER BY name")
    [conf.write("%s = %s\n" % (name, code)) for (name,code) in res]
#    for row in res:
#        conf.set('fieldnames',row[0],row[1])

def dump_tagnames(conf):
    conf.write("\n[tagnames]\n") 
#    conf.add_section("tagnames")
    res = run_sql("SELECT name,value FROM tag ORDER by value")
    [conf.write("%s = %s\n" % (val, name)) for (name,val) in res]
 #   for row in res:
 #       conf.set('fieldnames',row[1],row[0])



if __name__ == "__main__":
    main()
