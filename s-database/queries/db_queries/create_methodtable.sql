CREATE TABLE method_ids AS
SELECT FileName, Specifier, FunctionName, Stereotype, SplittedWords, GrammarPattern
from identifiers_table
WHERE FunctionName IS NOT NULL;