SELECT * FROM method_ids
WHERE GrammarPattern LIKE ' %NNP' AND Stereotype LIKE 'void-accessor collaborator '

SELECT * FROM method_ids
WHERE GrammarPattern LIKE ' VB% %NNP' AND Stereotype LIKE 'void-accessor collaborator '

SELECT * FROM method_ids
WHERE GrammarPattern LIKE ' JJ%' AND Stereotype LIKE 'void-accessor '

SELECT * FROM method_ids
WHERE GrammarPattern LIKE ' %NNP' AND Stereotype LIKE 'property collaborator '