doubling a = a + a

div2 a = div a 2

mul_ a b  
	| a == 0 || b == 0 = 0
	| sgn a == sgn b = mul1 (abs a) (abs b)
	| otherwise =  -(mul1 (abs a) (abs b))

mul1 a b
	|b == 1 = a
	|even b = (mul1.doubling) a (div2 b)
    |	otherwise  = (mul1 a (b-1)) + a
	
sgn x
	| x > 0  =  1
    | x == 0 =  0
    | otherwise  = -1