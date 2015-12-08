data Triple = Triple Int Int Int
x = Triple 1 1 1
-----
fn arg 
fn (Triple x y z)
-----
data T = Triad Int Int Int
printTriad t@(x y z) = pustStrLn ("first:" ++ (show x))
					>> pustStrLn ("second:" ++ (show y))
					
-----
data E = Example { first :: Int
					, second :: Int
					, third :: Int
				} deriving (Show)
				
{-
let e = Example {first = 1, second = 2, third = 3}
e
first e
let incFirst x = x {first first x + 1}
incFirst e
e { second = 10 }

-}				
-----
copyTextFile src dst = 
	catch ( readFile src >>= writeFile dst )
		  ( \err -> putStrLn (show err) )
-----
:t readFile
	:: String -> IO String
:t writeFile
	:: String -> String -> IO()
-----
Монада - абстракция линейной цепочки связанных вычислений.
Монада служит для инкапсуляции функций с побочным эффектом с целью их отделения от чистого кода.
Монада - это контейнерный тип.
-----
монада IO - это весь окружающий мир
Pure program <=> IO[Real world]
-----
монада Maybe
data Maybe a = Nothing | Just a
-----
let key = 1
:t (lookup key [(1,"one"), (2, "two"), (3, "three")])
:: Maybe String

value = case lookup key xs of
		Nothing -> 1
		Just x -> x
-----
Законы Монад:
1) согласованность оператора >>=
	return x >>= f тождественно f x
2) правило правой единицы 
	f >> return тождественно f
3) ассоциативность
	f >>= (g >>= h) тождественно (f >>= g ) >>= h 
-----
{-
class Monad m where
	(>>=) :: m a	-> (a -> m b) --required
	return :: a 	-> m a
	--other are optional
-}
-----
data Simple a = Simple a deriving (Show)

instance Monad Simple where
	return x 		= Simple x
	Simple x >>= fn = fn x
-----
доклады
Data.Random - это System.Random, блеать.
формализация функционального программирования на основе лямбда исчисления
-----
thinking forth
-----
взять доклад
