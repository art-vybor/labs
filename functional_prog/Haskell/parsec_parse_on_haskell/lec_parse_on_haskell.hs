{-
в форте:
РБНФ
word := не пробел, {не пробел}, пробел{пробел}.
quoted = ".", "\"",любой символ{...},пробел{пробел}.
-}

-----
Parsec - парсер в Haskell
import Text.ParserCombinators.Parsec

forthStc = "123  .  .\" abc   cde\" cr\n"

{-
РБНФ:

word := non-space, {non-space}, space, {space}.
quoted := dot, quote, space, {any}, quote, space, {space}.
-}

program :: Parser [[String]]

program = many1    -- один или много
	( try(quoted)  -- строка для печати
	<|> word )	   -- или просто слово
--порядок важен

quoted :: Parser[String]
quoted = do
	string ".\""
	space
	w <- many1 (noneOf "\"")
	char '"'
	space
	spaces
	return [".\"",w]

word :: Parser [String]
word = do
	w <- many1 (noneOf "\t\n\r\"")
	space
	spaces
	return [w]
	
	
test1 = case (parse program "") forthSrc of
	Left err -> print err
	Right ws -> print ws

----

{-
 (define (sum list1) (apply + list1))
 (define (average list1) (/ (sum list1) (length list1)))
 -}
 data Token = Atom String | List [Token] direving (Show)
 
 program :: Parser [Token]
 program = do
	spaces
	ls <- many1 (list <|> atom)
	spaces
	return ls

list :: Parser Token
list = do
	spaces
	char '('
	ls <- many1 (list <|> atom)
	char '('
	spaces
	return $ List ls

atom :: Parser Token
atom = do
	spaces
	a <- many1 (noneOf " \n\r\t\"()")
	spaces
	return $ Atom a
	
test = do
	src <- readFile "test2.scm"
	case (parse program "" src) of
		Left err -> print err
		Right ws -> print ws

----
задание 1
допилить компилятор форта
добавить поддержку строчных комментариев
задание 2

----		
		
http://legacy.cs.uu.nl/daan/parsec.html		
