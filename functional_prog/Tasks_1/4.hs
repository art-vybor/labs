--prime1 :: Integral a => a -> a
prime1 a
	| a == 1 = "prime"
	| otherwise = check a (div a 2)

check a b
	| b == 1 = "prime"
	| rem a b == 0 = "not prime"
	| otherwise = check a (b-1)