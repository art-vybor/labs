main = promt >> getLine >>= proc

promt = putStr "calc: " --приглашение

proc "" = return ()
proc line = return (calc (words line) []) >>= putStrLn >> promt >> getLine >>= proc
	
calc :: [String] -> [Double] -> String
calc 		[]		(x:[])	=	show x --результат
calc 	("+":ws)  	(y:x:xs)=	calc ws ( (x+y):xs )
calc 	("-":ws)  	(y:x:xs)=	calc ws ( (x-y):xs )
calc 	("*":ws)  	(y:x:xs)=	calc ws ( (x*y):xs )
calc 	("/":ws)  	(y:x:xs)=	calc ws ( (x/y):xs )
calc 	("^":ws)  	(y:x:xs)=	calc ws ( (x**y):xs )
--остальные операции также

calc ( _:[]) _ = "wrong"
calc (w:ws)  xs = calc ws ((read w):xs)

--есть ещё одна реализация в learn you a haskell	