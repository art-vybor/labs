-- Парсер *.csv файлов
import Text.ParserCombinators.Parsec
import System.Environment

main = getArgs >>= return . (!! 0)
				>>= readFile
 				>>= parseFile
				>>= print

parseFile inputFile = return result
		where 	Right result = parse file "" inputFile
		
{-
граматика в виде РБНФ
eol := "\n"
comma := ','
quote := '\"'
letters := ANY except (eol,comma)
quotesChar := ANY except comma | "\"\""
quoteCell := quote, {quotesChar}, quote
cell := quoteCell | {letters}
line := cell, {comma, cell}
file := line, {eol, line}
-}

eol = string "\n"
comma = char ','
quote = char '\"'
letters = noneOf ",\n"
quotesChar = noneOf "\"" <|> try (string "\"\"" >> return '\"')
quotesCell = do quote; _cell <- many quotesChar; quote;
				return _cell
cell = quotesCell <|> many letters
line = sepBy cell comma
file = sepBy line eol











