import csv
import requests
import xml.etree.ElementTree as ET
import os
import json
import subprocess
import sqlite3
import nltk
from spiral.simple_splitters import pure_camelcase_split
from spiral.simple_splitters import safe_simple_split

sqlite_file = '/Users/tejal/Desktop/Capstone/SCANL_tv_lex/lex-database/openRefine_results.db'
table_name = 'tagger_table'  # name of the table to be created
filename_field = 'FileName'
stereotype_field = 'Stereotype'
class_field = 'ClassName' # name of the column
function_field = 'FunctionName'
splittdWords_field = 'SplittedWords'
grammarPattern_field = 'GrammarPattern'
identifier_name = 'IdentifierName'
lexical_identifier_name = 'LexicalIdentifierName'
lexical_category = 'SCLC'

field_type = 'TEXT'  # column data type


def parseXML(xmlfile,file,c):
    #print(xmlfile)
    # create element tree object
    tree = ET.parse(xmlfile)
    # get root element
    root = tree.getroot()
    
    # create empty set for classidentifiers items
    identifiers = set()
    lex = dict() #dictionary to hold identifier name and lexical category.
    key = ''    
    lex_list = ['noun', 'pnoun', 'pronoun', 'adjective']
    lex_count = [0,0,0,0]
    # iterate news items
    for child in root:
        if child.tag == '{http://www.srcML.org/srcML/src}unit':
            for unit in child:
                if unit.tag == '{http://www.srcML.org/srcML/src}class':
                    stereotype=''
                    for classElements in unit:
                        if classElements.tag =='{http://www.srcML.org/srcML/src}name':
                            className = classElements.text
                        if classElements.tag =='{http://www.srcML.org/srcML/src}block':
                            for blockElements in classElements:
                                if blockElements.tag == '{http://www.srcML.org/srcML/src}stereotype':
                                    stereotype = blockElements.text 
                                if blockElements.tag == '{http://www.srcML.org/srcML/src}decl_stmt':
                                    for decl_stmt in blockElements:
                                        length = len(decl_stmt.getchildren())
                                        if decl_stmt.tag == '{http://www.srcML.org/srcML/src}decl':
                                            count = 0
                                            for declElements in decl_stmt:
                                                count += 1 
                                                if declElements.tag == '{http://www.srcML.org/srcML/src}name':
                                                    key = declElements.text
                                                # check if identifier name has lexical category.
                                                if count == length and key:
                                                    indx = declElements.tag.rfind('}')
                                                    lexEntry = declElements.tag[indx+1:]
                                                    if lexEntry in lex_list:
                                                        if lexEntry == 'noun':
                                                            lex_count[0] += 1
                                                        elif lexEntry == 'pnoun':
                                                            lex_count[1] += 1
                                                        elif lexEntry == 'pronoun':
                                                            lex_count[2] += 1
                                                        else:
                                                            lex_count[3] +=1
                                                        if key not in lex:
                                                            lex[key] = list()
                                                        if lexEntry not in lex[key]:
                                                            lex[key].append(lexEntry)
                                                    safeSimpleSplit_list = safe_simple_split(key)
                                                    grammar_pattern_list = nltk.pos_tag(safeSimpleSplit_list)
                                                    grammar_pattern=''
                                                    for w in grammar_pattern_list:
                                                        grammar_pattern = grammar_pattern+' '+w[1]
                                                    splittedWord=''
                                                    for word in safeSimpleSplit_list:
                                                        splittedWord=splittedWord+' '+word
                                                    query = "INSERT INTO {tn} ({fln},{sn},{cn},{idn},{wln},{pn}) VALUES('"+file+"','"+stereotype+"','"+str(className)+"','"+key+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                    c.execute(query.format(tn=table_name,fln=filename_field,sn=stereotype_field,cn= class_field,idn=identifier_name,wln=splittdWords_field,pn=grammarPattern_field))
                                if blockElements.tag == '{http://www.srcML.org/srcML/src}class':
                                    for innerClassElements in blockElements: 
                                        if innerClassElements.tag =='{http://www.srcML.org/srcML/src}name':
                                            innerClassName = innerClassElements.text
                                        if innerClassElements.tag == '{http://www.srcML.org/srcML/src}block':
                                            for innerBlock in innerClassElements:
                                                if innerBlock.tag == '{http://www.srcML.org/srcML/src}stereotype':
                                                    stereotype = innerBlock.text 
                                                if innerBlock.tag == '{http://www.srcML.org/srcML/src}decl_stmt':
                                                    for decl_stmt in innerBlock:
                                                        length = len(decl_stmt.getchildren())
                                                        if decl_stmt.tag == '{http://www.srcML.org/srcML/src}decl':
                                                            count = 0
                                                            for declElements in decl_stmt:
                                                                count += 1 
                                                                if declElements.tag == '{http://www.srcML.org/srcML/src}name':
                                                                    key = declElements.text
                                                                if count == length and key:
                                                                    indx = declElements.tag.rfind('}')
                                                                    lexEntry = declElements.tag[indx+1:]
                                                                    if lexEntry in lex_list:
                                                                        if lexEntry == 'noun':
                                                                            lex_count[0] += 1
                                                                        elif lexEntry == 'pnoun':
                                                                            lex_count[1] += 1
                                                                        elif lexEntry == 'pronoun':
                                                                            lex_count[2] += 1
                                                                        else:
                                                                            lex_count[3] +=1
                                                                        if key not in lex:
                                                                            lex[key] = list()
                                                                        if lexEntry not in lex[key]:
                                                                            lex[key].append(lexEntry)
                                                                    safeSimpleSplit_list = safe_simple_split(key)
                                                                    grammar_pattern_list = nltk.pos_tag(safeSimpleSplit_list)
                                                                    grammar_pattern=''
                                                                    for w in grammar_pattern_list:
                                                                        grammar_pattern = grammar_pattern+' '+w[1]
                                                                    splittedWord=''
                                                                    for word in safeSimpleSplit_list:
                                                                        splittedWord=splittedWord+' '+word
                                                                    query = "INSERT INTO {tn} ({fln},{sn},{cn},{idn},{wln},{pn}) VALUES('"+file+"','"+stereotype+"','"+str(innerClassName)+"','"+key+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                                    c.execute(query.format(tn=table_name,fln=filename_field,sn=stereotype_field,cn=class_field,idn=identifier_name,wln=splittdWords_field,pn=grammarPattern_field))
                                if blockElements.tag == '{http://www.srcML.org/srcML/src}function':
                                    for functionElements in blockElements:
                                        if functionElements.tag == '{http://www.srcML.org/srcML/src}name':
                                            functionName = functionElements.text
                                        if functionElements.tag =='{http://www.srcML.org/srcML/src}block':
                                            for functionBlockElements in functionElements:
                                                if functionBlockElements.tag =='{http://www.srcML.org/srcML/src}decl_stmt':
                                                    for decl_stmt in functionBlockElements:
                                                        length = len(decl_stmt.getchildren())
                                                        if decl_stmt.tag == '{http://www.srcML.org/srcML/src}decl':
                                                            count = 0
                                                            for declElements in decl_stmt:
                                                                count += 1 
                                                                if declElements.tag == '{http://www.srcML.org/srcML/src}name':
                                                                    key = declElements.text
                                                                if count == length and key:
                                                                    indx = declElements.tag.rfind('}')
                                                                    lexEntry = declElements.tag[indx+1:]
                                                                    if lexEntry in lex_list:
                                                                        if lexEntry == 'noun':
                                                                            lex_count[0] += 1
                                                                        elif lexEntry == 'pnoun':
                                                                            lex_count[1] += 1
                                                                        elif lexEntry == 'pronoun':
                                                                            lex_count[2] += 1
                                                                        else:
                                                                            lex_count[3] +=1
                                                                        if key not in lex:
                                                                            lex[key] = list()
                                                                        if lexEntry not in lex[key]:
                                                                            lex[key].append(lexEntry)
                                                                    safeSimpleSplit_list = safe_simple_split(key)
                                                                    grammar_pattern_list = nltk.pos_tag(safeSimpleSplit_list)
                                                                    grammar_pattern=''
                                                                    for w in grammar_pattern_list:
                                                                        grammar_pattern = grammar_pattern+' '+w[1]
                                                                    splittedWord=''
                                                                    for word in safeSimpleSplit_list:
                                                                        splittedWord=splittedWord+' '+word
                                                                    query = "INSERT INTO {tn} ({fln},{sn},{cn},{idn},{wln},{pn}) VALUES('"+file+"','"+stereotype+"','"+functionName+"','"+key+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                                    c.execute(query.format(tn=table_name,fln=filename_field,sn=stereotype_field,cn=function_field,idn=identifier_name, wln=splittdWords_field,pn=grammarPattern_field))
                                                if functionBlockElements.tag =='{http://www.srcML.org/srcML/src}for':
                                                    for forElements in functionBlockElements:
                                                        if forElements.tag == '{http://www.srcML.org/srcML/src}block':
                                                            for innerBlock in forElements:
                                                                if innerBlock.tag == '{http://www.srcML.org/srcML/src}decl_stmt':
                                                                    for decl_stmt in innerBlock:
                                                                        length = len(decl_stmt.getchildren())
                                                                        if decl_stmt.tag == '{http://www.srcML.org/srcML/src}decl':
                                                                            count = 0
                                                                            for declElements in decl_stmt:
                                                                                count += 1 
                                                                                if declElements.tag == '{http://www.srcML.org/srcML/src}name':
                                                                                    key = declElements.text
                                                                                if count == length and key:
                                                                                    indx = declElements.tag.rfind('}')
                                                                                    lexEntry = declElements.tag[indx+1:]
                                                                                    if lexEntry in lex_list:
                                                                                        if lexEntry == 'noun':
                                                                                            lex_count[0] += 1
                                                                                        elif lexEntry == 'pnoun':
                                                                                            lex_count[1] += 1
                                                                                        elif lexEntry == 'pronoun':
                                                                                            lex_count[2] += 1
                                                                                        else:
                                                                                            lex_count[3] +=1
                                                                                        if key not in lex:
                                                                                            lex[key] = list()
                                                                                        if lexEntry not in lex[key]:
                                                                                            lex[key].append(lexEntry)
                                                                                    safeSimpleSplit_list = safe_simple_split(key)
                                                                                    grammar_pattern_list = nltk.pos_tag(safeSimpleSplit_list)
                                                                                    grammar_pattern=''
                                                                                    for w in grammar_pattern_list:
                                                                                        grammar_pattern = grammar_pattern+' '+w[1]
                                                                                    splittedWord=''
                                                                                    for word in safeSimpleSplit_list:
                                                                                        splittedWord=splittedWord+' '+word
                                                                                    query = "INSERT INTO {tn} ({fln},{sn},{idn},{wln},{pn}) VALUES('"+file+"','"+stereotype+"','"+key+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                                                    c.execute(query.format(tn=table_name,fln=filename_field,sn=stereotype_field,cn=function_field,idn=identifier_name,wln=splittdWords_field,pn=grammarPattern_field))
                                                                if innerBlock.tag == '{http://www.srcML.org/srcML/src}try':
                                                                    for tryElements in innerBlock: 
                                                                        if tryElements.tag == '{http://www.srcML.org/srcML/src}block':
                                                                            for tryBlock in tryElements:
                                                                                if tryBlock.tag == '{http://www.srcML.org/srcML/src}decl_stmt':
                                                                                    for decl_stmt in tryBlock:
                                                                                        length = len(decl_stmt.getchildren())
                                                                                        if decl_stmt.tag == '{http://www.srcML.org/srcML/src}decl':
                                                                                            count = 0
                                                                                            for declElements in decl_stmt:
                                                                                                count += 1 
                                                                                                if declElements.tag == '{http://www.srcML.org/srcML/src}name':
                                                                                                    key = declElements.text
                                                                                                if count == length and key:
                                                                                                    indx = declElements.tag.rfind('}')
                                                                                                    lexEntry = declElements.tag[indx+1:]
                                                                                                    if lexEntry in lex_list:
                                                                                                        if lexEntry == 'noun':
                                                                                                            lex_count[0] += 1
                                                                                                        elif lexEntry == 'pnoun':
                                                                                                            lex_count[1] += 1
                                                                                                        elif lexEntry == 'pronoun':
                                                                                                            lex_count[2] += 1
                                                                                                        else:
                                                                                                            lex_count[3] +=1
                                                                                                        if key not in lex:
                                                                                                            lex[key] = list()
                                                                                                        if lexEntry not in lex[key]:
                                                                                                            lex[key].append(lexEntry)                                                                                                    
                                                                                                    safeSimpleSplit_list = safe_simple_split(key)
                                                                                                    safeSimpleSplit_list = safe_simple_split(key)
                                                                                                    grammar_pattern_list = nltk.pos_tag(safeSimpleSplit_list)
                                                                                                    grammar_pattern=''
                                                                                                    for w in grammar_pattern_list:
                                                                                                        grammar_pattern = grammar_pattern+' '+w[1]
                                                                                                    splittedWord=''
                                                                                                    for word in safeSimpleSplit_list:
                                                                                                        splittedWord=splittedWord+' '+word
                                                                                                    query = "INSERT INTO {tn} ({fln},{sn},{idn},{wln},{pn}) VALUES('"+file+"','"+stereotype+"','"+key+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                                                                    c.execute(query.format(tn=table_name,fln=filename_field,sn=stereotype_field,cn=function_field,idn=identifier_name,wln=splittdWords_field,pn=grammarPattern_field))
                                                if functionBlockElements.tag =='{http://www.srcML.org/srcML/src}try':
                                                    for tryElements in functionBlockElements: 
                                                        if tryElements.tag == '{http://www.srcML.org/srcML/src}block':
                                                            for tryBlock in tryElements:
                                                                if tryBlock.tag == '{http://www.srcML.org/srcML/src}decl_stmt':
                                                                    for decl_stmt in tryBlock:
                                                                        length = len(decl_stmt.getchildren())
                                                                        if decl_stmt.tag == '{http://www.srcML.org/srcML/src}decl':
                                                                            count = 0
                                                                            for declElements in decl_stmt:
                                                                                count += 1 
                                                                                if declElements.tag == '{http://www.srcML.org/srcML/src}name':
                                                                                    key = declElements.text
                                                                                if count == length and key:
                                                                                    indx = declElements.tag.rfind('}')
                                                                                    lexEntry = declElements.tag[indx+1:]
                                                                                    if lexEntry in lex_list:
                                                                                        if lexEntry == 'noun':
                                                                                            lex_count[0] += 1
                                                                                        elif lexEntry == 'pnoun':
                                                                                            lex_count[1] += 1
                                                                                        elif lexEntry == 'pronoun':
                                                                                            lex_count[2] += 1
                                                                                        else:
                                                                                            lex_count[3] +=1
                                                                                        if key not in lex:
                                                                                            lex[key] = list()
                                                                                        if lexEntry not in lex[key]:
                                                                                            lex[key].append(lexEntry)
                                                                                    safeSimpleSplit_list = safe_simple_split(key)
                                                                                    grammar_pattern_list = nltk.pos_tag(safeSimpleSplit_list)
                                                                                    grammar_pattern=''
                                                                                    for w in grammar_pattern_list:
                                                                                        grammar_pattern = grammar_pattern+' '+w[1]
                                                                                    splittedWord=''
                                                                                    for word in safeSimpleSplit_list:
                                                                                        splittedWord=splittedWord+' '+word
                                                                                    query = "INSERT INTO {tn} ({fln},{sn},{idn},{wln},{pn}) VALUES('"+file+"','"+stereotype+"','"+key+"','"+splittedWord+"','"+grammar_pattern+"')"
                                                                                    c.execute(query.format(tn=table_name,fln=filename_field,sn=stereotype_field,cn=function_field,idn=identifier_name,wln=splittdWords_field,pn=grammarPattern_field))                                                      
    #insert key value of dictionary in database.
    for k, v in lex.items():
        query = "INSERT INTO {tn} ({fln},{idn},{lc}) VALUES('"+file+"','"+k+"','"+' '.join(v)+"')"
        c.execute(query.format(tn=table_name,fln=filename_field,idn=lexical_identifier_name,lc=lexical_category))                                                      
    ET.register_namespace('','http://www.srcML.org/srcML/src')
    tree.write(xmlfile)
     
def main():
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute('CREATE TABLE {tn} ({nf} {ft})'\
        .format(tn=table_name, nf=filename_field, ft=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=stereotype_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=class_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=function_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=identifier_name, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=splittdWords_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=grammarPattern_field, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=lexical_identifier_name, ct=field_type))
    c.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}"\
        .format(tn=table_name, cn=lexical_category, ct=field_type))

    for root, dirs, files in os.walk("/Users/tejal/Desktop/Capstone/SCANL_tv_lex/lexical/lexical_output"):
        for file in files:
            if file.endswith(".xml"):
                parseXML(os.path.join(root, file),file,c)
                conn.commit()
    conn.close()
    
if __name__ == "__main__":
 
    # calling main function
    main()