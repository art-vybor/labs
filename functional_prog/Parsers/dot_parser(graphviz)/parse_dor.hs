-- Парсер *.dot файлов
import Text.ParserCombinators.Parsec
import System.Environment

main = getArgs >>= return . (!! 0)
	>>= readFile
	>>= parseFile
	>>= print

parseFile inputFile = case parse graph "" inputFile of
		Right a -> return a
		Left a -> return $ show a 
			
graph = do
	spaces
	type1 <- (string "graph" <|> string "digraph")
	spaces
	char '{'
	spaces
	smth_list
	spaces
	char '}'
	spaces
	return "it's graphviz file"
	
smth_list =	sepBy spaces smth -- sepBy divr stmt
smth = (try(edge) <|> node)

node = iD
edge = do
	iD
	edgeRHS
	
charOfID = noneOf "/ \t\n>=<\";"	
iD = many1 charOfID

edgeRHS = do
	spaces
	l <- (try(string "<-") <|> try(string "--") <|> string "->")
	
	-- edgeop
	spaces
	iD
	
-- edgeop = ( string "<-" <|> string "--" <|> string "->" )