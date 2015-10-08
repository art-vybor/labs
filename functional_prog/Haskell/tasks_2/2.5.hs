import Data.List

mid list n m	| length( list ) < n = []
				| otherwise = drop (n-1) (take (n - 1 + m) list)