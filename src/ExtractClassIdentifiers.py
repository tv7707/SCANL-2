import csv
import requests
import xml.etree.ElementTree as ET
import os
import subprocess
import sqlite3
import nltk
from spiral.simple_splitters import pure_camelcase_split

sqlite_file = '/Users/tejal/Desktop/Capstone/SCANL_tv_lex/s-database/wycheproof_result.db'
table_name = 'identifiers_table'  # name of the table to be created
filename_field = 'FileName'
class_field = 'ClassName' # name of the column
function_field = 'FunctionName'
stereotype_field = 'Stereotype'
specifier_field = 'Specifier'
variable_field = 'Variable'
splittdWords_field = 'SplittedWords'
grammarPattern_field = 'GrammarPattern'
field_type = 'TEXT'  # column data type

def parseXML(xmlfile,file,c):
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
      
    identifiers = {}
    identifiers = set()
    # iterate news items
    for child in root:
        if child.tag == '{http://www.srcML.org/srcML/src}unit':
            for unit in child:
                if unit.tag == '{http://www.srcML.org/srcML/src}class':
                    specifier=''
                    stereotype=''
                    for classElements in unit:
                        if classElements.tag =='{http://www.srcML.org/srcML/src}specifier':
                            if classElements.text != None:
                                specifier = classElements.text
                        if classElements.tag =='{http://www.srcML.org/srcML/src}name':
                            if classElements.text != None:
                                if classElements.text not in identifiers:
                                    splittedList = pure_camelcase_split(classElements.text)
                                    grammar_pattern_list = nltk.pos_tag(splittedList)
                                    grammar_pattern=''
                                    for w in grammar_pattern_list:
                                        grammar_pattern = grammar_pattern+' '+w[1]
                                    splittedWord=''
                                    for word in splittedList:
                                        splittedWord=splittedWord+' '+word
                                    query = "INSERT INTO {tn} ({fln},{sn},{cn},{wln},{pn}) VALUES('"+file+"','"+specifier+"','"+str(classElements.text)+"','"+splittedWord+"','"+grammar_pattern+"')"
                                    c.execute(query.format(tn=table_name,fln=filename_field,sn=specifier_field,cn=class_field,wln=splittdWords_field,pn=grammarPattern_field))
                                    el = ET.SubElement(classElements,'grammar_pattern')
                                    el.text = grammar_pattern
                        if classElements.tag =='{http://www.srcML.org/srcML/src}block':
                            for blockElements in classElements:
                                if blockElements.tag == '{http://www.srcML.org/srcML/src}stereotype':
                                    stereotype = blockElements.text
                                if blockElements.tag == '{http://www.srcML.org/srcML/src}function':
                                    for functionElements in blockElements:
                                        if functionElements.tag =='{http://www.srcML.org/srcML/src}specifier':
                                            if functionElements.text != None:
                                                specifier = functionElements.text
                                        if functionElements.tag == '{http://www.srcML.org/srcML/src}name':
                                            if functionElements.text not in identifiers:
                                                identifiers.add(functionElements.text)
                                                functionName = functionElements.text
                                                splittedList = pure_camelcase_split(functionElements.text)
                                                grammar_pattern_list = nltk.pos_tag(splittedList)
                                                grammar_pattern=''
                                                for w in grammar_pattern_list:
                                                    grammar_pattern = grammar_pattern+' '+w[1]
                                                splittedWord=''
                                                for word in splittedList:
                                                    splittedWord=splittedWord+' '+word
                                                query = "INSERT INTO {tn} ({fln},{sn},{cn},{stn},{wln},{pn}) VALUES('"+file+"','"+specifier+"','"+str(functionElements.text)+"','"+stereotype+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                c.execute(query.format(tn=table_name,fln=filename_field,sn=specifier_field, cn=function_field,stn=stereotype_field,wln=splittdWords_field,pn=grammarPattern_field))
                                                el = ET.SubElement(functionElements,'grammar_pattern')
                                                el.text = grammar_pattern
                                        if functionElements.tag =='{http://www.srcML.org/srcML/src}block':
                                            for functionBlockElements in functionElements:
                                                if functionBlockElements.tag =='{http://www.srcML.org/srcML/src}expr_stmt':
                                                    for expr_stmtElements in functionBlockElements:
                                                        if expr_stmtElements.tag =='{http://www.srcML.org/srcML/src}expr':
                                                            for exprElements in expr_stmtElements:
                                                                if exprElements.tag =='{http://www.srcML.org/srcML/src}call':
                                                                    for callElements in exprElements:
                                                                        if callElements.tag =='{http://www.srcML.org/srcML/src}name':
                                                                            for nameElements in callElements:
                                                                                if nameElements.tag =='{http://www.srcML.org/srcML/src}name':
                                                                                    if nameElements.text != 'this' and nameElements.text != None:
                                                                                        splittedList=pure_camelcase_split(nameElements.text)
                                                                                        grammar_pattern_list = nltk.pos_tag(splittedList)
                                                                                        grammar_pattern=''
                                                                                        for w in grammar_pattern_list:
                                                                                            grammar_pattern = grammar_pattern+' '+w[1]
                                                                                        splittedWord=''
                                                                                        for word in splittedList:
                                                                                            splittedWord=splittedWord+' '+word
                                                                                        query = "INSERT INTO {tn} ({fln},{vn},{wln},{pn}) VALUES('"+file+"','"+str(nameElements.text)+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                                                        c.execute(query.format(tn=table_name,fln=filename_field,cn=function_field,vn=variable_field,wln=splittdWords_field,pn=grammarPattern_field))
                                                                                        el = ET.SubElement(nameElements,'grammar_pattern')
                                                                                        el.text = grammar_pattern
                                                                                                
                                if blockElements.tag == '{http://www.srcML.org/srcML/src}class':
                                    for classElements in child:
                                        if classElements.tag =='{http://www.srcML.org/srcML/src}name':
                                            if classElements.text != None:
                                                if classElements.text not in identifiers:
                                                    identifiers.add(classElements.text)
                                                    splittedList=pure_camelcase_split(classElements.text)
                                                    splittedWord=''
                                                    for word in splittedList:
                                                        splittedWord=splittedWord+' '+word
                                                    grammar_pattern_list = nltk.pos_tag(splittedList)
                                                    grammar_pattern=''
                                                    for w in grammar_pattern_list:
                                                        grammar_pattern = grammar_pattern+' '+w[1]
                                                    query = "INSERT INTO {tn} ({fln},{cn},{wln},{pn}) VALUES('"+file+"','"+str(classElements.text)+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                    c.execute(query.format(tn=table_name, fln=filename_field,cn=class_field,wln=splittdWords_field,pn=grammarPattern_field))
                                                    el = ET.SubElement(classElements,'grammar_pattern')
                                                    el.text = grammar_pattern
    ET.register_namespace('','http://www.srcML.org/srcML/src')
    tree.write(xmlfile)
     
def main():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name, nf=filename_field, ft=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=specifier_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=class_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=function_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=stereotype_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=variable_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=splittdWords_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=grammarPattern_field, ct=field_type))

    for root, dirs, files in os.walk("/Users/tejal/Desktop/Capstone/SCANL_tv_lex/lexical/lexical_output/"):
        for file in files:
            if file.endswith(".xml"):
                parseXML(os.path.join(root, file),file,c)
                conn.commit()
    conn.close()
    
if __name__ == "__main__":
 
    # calling main function
    main()