import Data.List

-- печатает 3 квартиля
quart a' | even $ length a = show (getfirst a) ++ " " ++ show (med a) ++ " " ++ show(getthird a 1)
	     | otherwise = show (getfirst a) ++ " " ++ show (med a) ++ " " ++ show(getthird a 2)
	where a = sort a'

--печатает интеркварльный размах
quartdiv a' | even $ length a = getthird a 1 - getfirst a
			| otherwise = getthird a 2 - getfirst a
	where a = sort a'

--печатает всё вылетающее из интеквартильного размаха
far a' = [x | x <- a, x < med a - 1.5 * quartdiv a || x > med a + 1.5 * quartdiv a  ]
	where a = sort a'

getfirst a = (med (mid a 0 (div (length a) 2 + 1)))
getthird a t = med(mid a ((div (length a) 2 + t)) (div (length a) 2))

med a | even $ length a = ((a !! m - 1) + (a !! m)) / 2  
		 | otherwise = a !! m
	where  m = div (length a) 2

mid list n m	| length( list ) < n = []
				| otherwise = drop (n-1) (take (n - 1 + m) list)