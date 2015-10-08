--тип данных - отрезок

data Seg' = Seg Double Double
	deriving(Show)

--основные арифметические операции
add' (Seg a b) (Seg c d) = Seg (a + c) (b + d)	
sub' (Seg a b) (Seg c d) = Seg (a - d) (b - c)	
mul' (Seg a b) (Seg c d) = Seg (minimum [a * c, a * d, b * c, b * d]) (maximum [a * c, a * d, b * c, b * d])
div' (Seg a b) (Seg c d) = Seg (minimum [a / c, a / d, b / c, b / d]) (maximum [a / c, a / d, b / c, b / d])

f1 a b = div' (mul' a b)(add' a b)
f2 a b = div' e (add' (div' e a) (div' e b))
	where e = Seg 1 1