import System.Environment
import Data.Char
import Data.Map
import Text.ParserCombinators.Parsec

-- readWs fp = readFile fp >>= map words . lines


main = getArgs >>= return . (!! 0)
				>>= readFile
 				>>= parseAll
				-- >>= print
				>>= clearAllBraces
				>>= go

-- Тип данных				 
data Tss = TssCreator { word 		:: [String],
						counter 	:: Int,
						dataS		:: [Int],
						funcS		:: [Int],
						loopS		:: [Int],
						ifDepth		:: Int,
						funcMassive	:: [(String, Int)]
					}
-- / Тип данных				 
				 
-- Удаление скобок		
--это быдло код, написать как и с loop		
clearAllBraces a = return (clrBraces a 0)

clrBraces a i 
			| length a == i = a
			| a !! i == "(" = clrBraces (remBrace (remove a i) i 1) i
			| otherwise = clrBraces a (i+1)

remBrace list n balance
			| balance == 0 = list
			| list !! n == "(" = remBrace (remove list n) n (balance+1)
			| list !! n == ")" = remBrace (remove list n) n (balance-1)
			| otherwise = remBrace (remove list n) n balance

remove list n = begin ++ drop 1 end
	where (begin,end) = splitAt n list
-- / Удаление скобок	

-- Парсинг				

-- / Парсинг

-- Выполнение программы
go a = exec TssCreator { word = a, counter = 0, dataS = [], funcMassive = [], funcS = [], ifDepth = 0, loopS = [] }			

exec tss
	| isEnd 		= return ()
	| isFuncStart 	= return (tss {funcMassive = (allWord !! (i+1), i+2) : funcMassive tss}) >>= skipToFuncEnd >>= exec
	| isInt 		= push curElem tss 			>>= next >>= exec
	| isUserFunc 	= runFunc curElem tss 		 		 >>= exec
	| isFuncEnd 	= ret tss 					>>= next >>= exec
	| isIf 			= runIf tss 				>>= next >>= exec
	| isElse		= skipWay (incCounter tss)	>>= next >>= exec
	| isThen		= return tss 				>>= next >>= exec
	| isDo			= runDo tss					>>= next >>= exec
	| isLoop		= runLoop tss				>>= next >>= exec
	| isI			= pushI tss					>>= next >>= exec
	| isLeave		= skipLoop tss				>>= next >>= exec
	| otherwise 	= builtin curElem tss 		>>= next >>= exec
	where
		i 			= counter tss
		allWord 	= word tss
		curElem 	= allWord !! i
		
		isEnd 		= i == length allWord
		isFuncStart = curElem == ":"
		isInt 		= checkInt curElem
		isUserFunc 	= check curElem (funcMassive tss)
		isFuncEnd 	= curElem == ";"
		isIf 		= curElem == "if"
		isElse 		= curElem == "else"
		isThen		= curElem == "then"
		isDo		= curElem == "do"
		isI			= (curElem == "i") && (not $ Prelude.null (loopS tss))
		isLoop		= curElem == "loop"
		isLeave		= curElem == "leave"
		
---- функции работы с циклами
pushI tss = return tss {dataS = ((loopS tss) !! 0) : (dataS tss)}

runLoop tss
	| loopSt !! 0 == (loopSt !! 1 - 1) = return tss {loopS = drop 3 (loopS tss)}
	| otherwise = return tss {counter = loopSt !! 2, loopS = ((loopSt !! 0) + 1):(drop 1 loopSt)}
	where
		loopSt = loopS tss

runDo tss = return tss {loopS = ((dataS tss) !! 0):((dataS tss) !! 1):(counter tss):(loopS tss), dataS = drop 2 (dataS tss)}

skipLoop tss = return tss {counter = findLoop tss (counter tss), loopS = drop 3 (loopS tss)} 

findLoop tss i
	| curElem == "do" 	= findLoop tss ((findLoop tss (i+1)) + 1) 
	| curElem == "loop" = i
	| otherwise 		= findLoop tss (i+1)
	where
		curElem			= (word tss) !! i
---- / функции работы с циклами		

---- функции работы с условиями
runIf tss
	| condition == 0 		= skipWay $ incCounter (tss {dataS = curS})
	| otherwise 			= return tss {dataS = curS}
	where
		([condition],curS) 	= splitAt 1 (dataS tss)	
	
skipWay tss
	| curElem == "if" 							= skipIf $ incCounter tss
	| curElem == "else" || curElem == "then" 	= return tss
	| otherwise 								= skipWay $ incCounter tss
	where
		curElem 								= (word tss) !! (counter tss)

skipIf tss 
	| curElem == "if" 	= skipIf $ incCounter tss
	| curElem == "then" = return $ incCounter tss
	| otherwise 		= skipIf $ incCounter tss
	where
		curElem			= (word tss) !! (counter tss)
---- / функции работы с условиями

---- next element
incCounter tss = tss {counter = counter tss + 1}			
next tss = return $ incCounter tss
---- / next element

---- push int to stack
push w tss = return tss {dataS = (read w):(dataS tss)}				
---- / push int to stack

---- user func support
check func map = not (Prelude.null [x | x <- map, fst x == func])
runFunc func tss = return tss {funcS = (counter tss):(funcS tss), counter = snd curFunc}
	where [curFunc] = [x | x <- funcMassive tss, fst x == func]	
ret tss = return tss {counter = (funcS tss) !! 0, funcS = drop 1 (funcS tss)}

skipToFuncEnd tss
			| (word tss) !! (counter tss) == ";" = return tss {counter = counter tss + 1}
			| counter tss == length (word tss) = return tss
			| otherwise = skipToFuncEnd tss {counter = counter tss + 1}
---- / user func support		

---- checkInt		
checkInt str
		| length str == 1 = isDigit first
		| first == '+' || first == '-' || isDigit first = onlyDigits $ drop 1 str
		| otherwise = False
		where first = str !! 0

onlyDigits "" = True
onlyDigits str 
			| isDigit $ str !! 0 = onlyDigits $ drop 1 str
			| otherwise = False
---- / checkInt		

---- builtin func support
builtin ">" tss = boolOp (>) tss
builtin "<" tss = boolOp (<) tss
builtin ">=" tss = boolOp (>=) tss
builtin "<=" tss = boolOp (<=) tss
builtin "==" tss = boolOp (==) tss
builtin "!=" tss = boolOp (/=) tss

builtin "*" tss = binOp (*) tss
builtin "+" tss = binOp (+) tss
builtin "-" tss = binOp (-) tss
builtin "/" tss = binOp (div) tss
builtin ".s" tss = print (dataS tss) >> return tss
builtin ".\"" tss = print (word tss !! (counter tss +1)) >> return tss {counter = counter tss + 1}
builtin "." tss = print (dataS tss !! 0) >> return tss {dataS = drop 1 (dataS tss)}
builtin "dup" tss = return tss {dataS = (dataS tss !! 0):(dataS tss)}
builtin "swap" tss = return tss {dataS = (dataS tss !! 1):(dataS tss !! 0):(drop 2 (dataS tss))}
builtin "drop" tss = return tss {dataS = drop 1 (dataS tss)}
builtin "true" tss = return tss {dataS = (-1):(dataS tss)}
builtin "false" tss = return tss {dataS = (0):(dataS tss)}
builtin w tss = print ("unrecognized: " ++ w) >> return tss

boolOp op tss = return  tss {dataS = (boolToInt result):(drop 2 (dataS tss))}		
	where 	
		result 	= op x  y
		x 		= (dataS tss) !! 1
		y 		= (dataS tss) !! 0

boolToInt True = -1
boolToInt False = 0

binOp op tss = return  tss {dataS = (result):(drop 2 (dataS tss))}		
	where 	
		result 	= op x  y
		x 		= (dataS tss) !! 1
		y 		= (dataS tss) !! 0
---- /builtin	

-- / Выполнение программы

----
parseAll textFile = return $ concat word
	where
		Right word = parse program "" (textFile ++ "\n")
-- парсинг
program :: Parser [[String]]

program = many1    -- один или много
	( try(quoted)  -- строка для печати
	<|> try(comment) --коментарий в одну строку
	<|> singleWord )	   -- или просто слово
--порядок важен

quoted :: Parser [String]
quoted = do
	string ".\""
	space
	w <- many1 (noneOf "\"")
	char '\"'
	space
	spaces
	return [".\"",w]

singleWord :: Parser [String]
singleWord = do
	w <- many1 (noneOf " \"\t\n\r")
	space
	spaces
	return [w]
	
comment :: Parser [String]
comment = do
	string "\\"
	w <- many1 (noneOf "\n")
	char '\n'
	space
	spaces
	return []
