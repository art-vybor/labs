f x = x * x

t = (sqrt(5)-1)/2

len a b = b - a

x1 a b = a + (1-t)* (len a b)
x2 a b = a + t * (len a b)

min' a b 
	| len (x1 a b) (x2 a b) < 0.0000001 = x1 a b
	| (x1.f) a b < (x2.f) a b = min' a (x2 a b)
	| otherwise = min' (x1 a b) b