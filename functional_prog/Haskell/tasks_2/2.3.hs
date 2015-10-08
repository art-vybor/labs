--prime1 :: Integral a => a -> a

--getnext :: Ord a => [a]->[a]

check a b = null $ filter (\x -> (rem b x == 0)) a
          
getnext a b | check a b = a ++ [b]
            | otherwise = getnext a (b+2)

            
getlistprime n a | n == 2 = a
	 | otherwise = getlistprime (n-1) (getnext a ((maximum a)+2))

getprime m n = drop (m-1) (getlistprime (m+n-1) [2,3])


