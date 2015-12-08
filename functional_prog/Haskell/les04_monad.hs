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
������ - ���������� �������� ������� ��������� ����������.
������ ������ ��� ������������ ������� � �������� �������� � ����� �� ��������� �� ������� ����.
������ - ��� ������������ ���.
-----
������ IO - ��� ���� ���������� ���
Pure program <=> IO[Real world]
-----
������ Maybe
data Maybe a = Nothing | Just a
-----
let key = 1
:t (lookup key [(1,"one"), (2, "two"), (3, "three")])
:: Maybe String

value = case lookup key xs of
		Nothing -> 1
		Just x -> x
-----
������ �����:
1) ��������������� ��������� >>=
	return x >>= f ������������ f x
2) ������� ������ ������� 
	f >> return ������������ f
3) ���������������
	f >>= (g >>= h) ������������ (f >>= g ) >>= h 
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
�������
Data.Random - ��� System.Random, ������.
������������ ��������������� ���������������� �� ������ ������ ����������
-----
thinking forth
-----
����� ������
