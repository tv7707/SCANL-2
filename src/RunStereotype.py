import os
import subprocess

def main():
    for root, dirs, files in os.walk("/Users/tejal/Desktop/Capstone/SCANL_tv_lex/lexical"):
        for file in files: 
            if file.endswith(".xml"):
                subprocess.call(["xsltproc","stereotype.xsl","/Users/tejal/Desktop/Capstone/SCANL_tv_lex/lexical/"+file,"--output","/Users/tejal/Desktop/Capstone/SCANL_tv_lex/lexical/lexical_output/"+file])
        print("Done "+file)
if __name__ == "__main__":
 
    # calling main function
    main()
