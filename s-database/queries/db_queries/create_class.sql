CREATE TABLE class_ids AS
SELECT FileName, Specifier, ClassName, SplittedWords, GrammarPattern
from identifiers_table
WHERE ClassName IS NOT NULL;