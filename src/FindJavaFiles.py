#This file will look at java files and convert them into xml using srcml
import os
import subprocess
for root, dirs, files in os.walk("/Users/tejal/Desktop/capstone_input/Telegram-master"):
    for file in files:
        if file.endswith(".java"):
            print(os.path.join(root, file))
            #subprocess takes 4 argument
            #1. path to srcml
            #2. java file path
            #3. output command
            #4. path where output will be stored.
            subprocess.run(["/usr/local/bin/srcml", os.path.join(root, file),"-o","/Users/tejal/Desktop/capstone_input/Telegram-srcML/"+file+".xml"])