#Analysis of source code using lexical categories and NLTK.

1. Download srcml from https://www.srcml.org/
2. Download NLTK from https://www.nltk.org/
3. Download spiral for splitting identifiers https://github.com/casics/spiral
4. To install srcMLPOSTagger follow these steps:
	4.a. install cmake
	4.b. install libxml2
	4.c. Clone repository with recursive to get submodules -- git clone https://github.com/srcML/srcMLPOSTagger --recursive
	4.d. Make a build folder inside of the srcMLPOSTagger folder -- mkdir build
	4.e. enter the build folder -- cd build
	4.f. cmake the project in the parent directory -- cmake ..
	4.g. make the project -- make
5. Clone the repository from github. 
6. To run the project:
	6.a. Make an input folder -- mkdir input
	6.b. Make an output folder -- mkdir srcmlOutput
	6.c  Make another output folder -- mkdir finalOutput
	6.d  Make database folder -- mkdir database 
7. Put Java project in input folder. 
8. Enter the src folder of cloned github repository and run the code: python FindJavaFiles.py.
#This file will transform you java files into xml format. Change the path to your srcml, input java project and output folder. 
9. Once all the files are converted to xml format. Run the code from src folder: python RunStereotype.py
# This file will add stereotypes in xml code. Change path to your srcmlOutput and finalOutput folder.
10. Run the code from src folder: python ExtractClassIdentifier.py
#This file will extract all the identifier and tag them with NLTK and insert the result into a SQLite database.Change the path to your finalOutput and database folder.
11. To tag xml file using srcMLPOSTagger run the code by redirecting from stdin -- ./bin/lexicalsmarkup < file.xml 	
11. Run the code from src folder: pyhton ExtractLexicalCategory.py
#This file will extract all the identifiers tagged by srcMLPosTagger. This file will also tag the identiifer with NLTK and insert them to SQLite database.Change the path to your finalOutput and database folder.