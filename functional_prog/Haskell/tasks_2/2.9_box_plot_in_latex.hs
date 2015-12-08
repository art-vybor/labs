module BoxPlot (
	printToFile
) where

import Data.List
import System.IO

---------
-- функции для работы с выводом
---------
-- печатает в файл ящик с усами
printToFile list fileName = do
	file <- openFile (fileName ++ ".tex") WriteMode 
	hPutStr file (content list)
	hClose file

-- формирует данные для печати
content list = "\\begin{document}\n" ++
	"\\setlength{\\unitlength}{1mm}\n" ++
	"\\begin{picture}(120,30)\n" ++
		"\\linethickness{0.3mm}\n" ++
	
	-- рисуем коробку	
		"\\put(62.5, 17.5) {\\line(1,0){25}}\n" ++
		"\\put(62.5, 32.5) {\\line(1,0){25}}\n" ++
		
		"\\linethickness{0.45mm}\n" ++
		"\\put(62.5, 17.5) {\\line(0,1){15}}\n" ++
		"\\put(" ++ show midLineX ++ ", 17.5) {\\line(0,1){15}}\n" ++
		"\\put(87.5, 17.5) {\\line(0,1){15}}\n" ++
	-- рисуем усы
		"\\put(" ++ show mustacheLineStart ++ ", 25) {\\line(1,0){75}}\n" ++
		"\\linethickness{0.6mm}\n" ++
		"\\put(" ++ show mustacheLineStart ++ ", 20) {\\line(0,1){10}}\n" ++
		"\\put(" ++ show mustacheLineEnd ++ ", 20) {\\line(0,1){10}}\n" ++
	--рисуем далёкие точки
		printFar list ++
		printNotSoFar list ++
	"\\end{picture}\n" ++
	"\\end{document}"
	where
		midLineX = getDotX list (getMiddle list)
		mustacheLineStart = midLineX - 25 * 1.5
		mustacheLineEnd = mustacheLineStart + 75

-- координата по Х для точки
getDotX list dot = 67.5 + (25 * (dot - getFirst list)) / (quartdiv list)		

-- печать далёких точек	
printFar list = printDots list (far list) 0 "" "*"
printNotSoFar list = printDots list (notSoFar list) 0 "" ""

-- печать точки
printDots _list list i curPict kindOfDot
	| i == length list = curPict
	| otherwise = printDots _list list (i+1) (curPict ++ (printDot _list (list !! i)) kindOfDot) kindOfDot

printDot list dot kindOfDot = "\\put(" ++ (show dotX) ++ ", 25) {\\circle" ++ kindOfDot ++ "{3}}\n"
	where dotX = getDotX list dot
---------
	
---------
-- функции для работы с квартилями
---------
-- печатает 3 квартиля
printQuart a' = show (getFirst a) ++ " " ++ show (getMiddle a) ++ " " ++ show(getThird a)
	where a = sort a'

-- печатает интерквартильный размах
quartdiv a' = getThird a - getFirst a
	where a = sort a'

-- печатает всё вылетающее из интеквартильного размаха
far a' = [x | x <- a, x < getMiddle a - 1.5 * quartdiv a || x > getMiddle a + 1.5 * quartdiv a  ]
	where a = sort a'
	
-- не такие далекие вылеты
notSoFar a' = [x | x <- a, x >= getMiddle a - 1.5 * quartdiv a && x < getFirst a || x <= getMiddle a + 1.5 * quartdiv a  && x > getThird a  ]
	where a = sort a'

--функции получения квартилей
getFirst a = (getMiddle (mid a 0 (div (length a) 2 + 1)))

getThird a  | even (length a) = getthird1 a 1
			| otherwise = getthird1 a 2
getthird1 a t = getMiddle (mid a ((div (length a) 2 + t)) (div (length a) 2))


getMiddle a | even $ length a = ((a !! m - 1) + (a !! m)) / 2  
			| otherwise = a !! m
	where  m = div (length a) 2

mid list n m	| length( list ) < n = []
				| otherwise = drop (n-1) (take (n - 1 + m) list)		
---------