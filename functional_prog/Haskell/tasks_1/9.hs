import Data.List

med a | even $ length a = ((a !! m - 1) + (a !! m)) / 2  
	  | otherwise = a !! m
	where  m = div (length a) 2
