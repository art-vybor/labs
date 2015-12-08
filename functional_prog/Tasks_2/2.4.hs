f1 a = a

rangeB a b d | b > a = range1 a b d [] f1
             | otherwise = range1 a b d [] not

range1 a b d c f |  ( a == b ) || ( f $ a > b ) = c
                 | otherwise = range1 (a+d) b d (c++[a]) f
				 
rangeA :: Integral a => a -> a -> a -> [a]

rangeA = rangeB
