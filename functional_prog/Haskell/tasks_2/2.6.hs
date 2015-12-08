compare_length x y = length x > length y

compare_1_and_3 x y | x !! 0 > y !! 0 = True
					| x !! 0 < y !! 0 = False
					| x !! 2 > y !! 2 = True
					| x !! 2 < y !! 2 = False
					| otherwise = True
--qsort :: [String] -> (String -> String -> Bool) -> [String] 

qsort a f | a == [] = []
		  | otherwise =  qsort [y| y <- xs, f x y ] f ++ [x] ++ qsort [y | y <- xs, not $ f x y] f
		where ([x],xs) = splitAt 1 a