-- Парсер *.xml файлов
import Text.ParserCombinators.Parsec
import System.Environment

main = getArgs >>= return . (!! 0)
	>>= readFile
	>>= parseFile
	>>= print

parseFile inputFile = return result
	where Right result = parse file "" inputFile

--------------------------------------
-- класс Tree ------------------------
--------------------------------------

data Tree = TreeCreator { name :: String, fields :: [Tree] }

instance Show Tree where
	show = treeToStr

treeToStr tree = _treeToStr tree ""

_treeToStr tree tab = (name tree) ++ "\n" ++ (treeListToStr (fields tree) (tab ++ "\t"))	

treeListToStr [] tab = ""
treeListToStr (curTree:listOfTree) tab
	| take 4 (name curTree) == "<!--" = ""
	| otherwise = tab ++ (_treeToStr curTree tab) ++ treeListToStr listOfTree tab

--------------------------------------
-- пример дерева ---------------------
--------------------------------------

a = TreeCreator {name = "a", fields = [ab,ac]}
ab = TreeCreator {name = "ab", fields = [aba,abb,abc]}
ac = TreeCreator {name = "ac", fields = [aca]}
aca = TreeCreator {name = "aca", fields = []}
aba = TreeCreator {name = "aba", fields = [abaa]}
abaa = TreeCreator {name = "abaa", fields = []}
abb = TreeCreator {name = "abb", fields = []}
abc = TreeCreator {name = "abc", fields = []}

{-
граматика в виде РБНФ
http://www.jelks.nu/XML/xmlebnf.html#NT-S
-}
---------------			

lt = char '<'
gt = char '>'

charOfName = noneOf "/ \t\n>=<\""

slash = char '/'

whiteSpace = many (oneOf " \t\n")

quote = char '\"'

simpleSymbol = noneOf "></"

simpleWord :: Parser Tree
simpleWord = do
	smth <- many1 simpleSymbol
	return TreeCreator {name = smth, fields = []}

element1 :: Parser Tree
element1 = try (element) <|> try (emptyElementTag) <|> try (comment) <|> simpleWord

attrField = do
	smth <- many (noneOf "\"")
	return TreeCreator {name = smth, fields = []}
	
attribute :: Parser Tree
attribute = do
	name <- many1 charOfName
	char '='
	quote
	field <- attrField
	quote
	return TreeCreator {name = name, fields = [field]}

startTag = do
	lt
	name <- many1 charOfName
	whiteSpace
	fields <- endBy attribute whiteSpace
	gt
	return TreeCreator {name = name, fields = fields}	

comment = do
	string "<!--"		
	comm <- many (noneOf "-")
	string "-->"
	return TreeCreator {name = "<!--" ++ comm, fields = []}	
	
endTag name = do
	lt
	slash
	string name
	gt
	
emptyElementTag = do
	lt	
	name <- many1 charOfName
	whiteSpace
	fields <- endBy attribute whiteSpace
	slash
	gt
	
	return TreeCreator {name = name, fields = fields}

element :: Parser Tree
element = do
	tree <- startTag
	whiteSpace
	fields1 <- endBy element1 whiteSpace
	endTag $ name tree
	return TreeCreator {name = name tree, fields = (fields tree) ++ fields1}	

file = element













