main = promt >> getLine >>= proc

promt = putStr "calc: " --�����������

proc "" = return ()
proc line = return (calc (words line) []) >>= putStrLn >> promt >> getLine >>= proc
	
calc :: [String] -> [Double] -> String
calc 		[]		(x:[])	=	show x --���������
calc 	("+":ws)  	(y:x:xs)=	calc ws ( (x+y):xs )
calc 	("-":ws)  	(y:x:xs)=	calc ws ( (x-y):xs )
calc 	("*":ws)  	(y:x:xs)=	calc ws ( (x*y):xs )
calc 	("/":ws)  	(y:x:xs)=	calc ws ( (x/y):xs )
calc 	("^":ws)  	(y:x:xs)=	calc ws ( (x**y):xs )
--��������� �������� �����

calc ( _:[]) _ = "wrong"
calc (w:ws)  xs = calc ws ((read w):xs)

--���� ��� ���� ���������� � learn you a haskell	