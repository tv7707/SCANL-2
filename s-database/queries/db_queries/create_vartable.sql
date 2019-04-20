CREATE TABLE variable_ids AS
SELECT FileName, Variable, SplittedWords, GrammarPattern
from identifiers_table
WHERE Variable IS NOT NULL;