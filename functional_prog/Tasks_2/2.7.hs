f x = x * x

t = (sqrt(5)-1)/2

top = 3

len a b = b - a

x1 a b = a + (1-t)* (len a b)
x2 a b = a + t * (len a b)

minA a b = min' a b (top-1)

min' a b i
	| i < 0 = do putStr "answer: "; return (x1 a b)
	| len (x1 a b) (x2 a b) < 0.0000001 = do putStr "answer: "; return (x1 a b)
	| f (x1 a b) < f (x2 a b) = do putStrLn $ show (x1 a b) ++ " to " ++ show (x2 a b) ; min' a (x2 a b) (i-1)
	| otherwise = do putStrLn $ show (x1 a b) ++ " to " ++ show (x2 a b) ; min' (x1 a b) b (i-1)


	
