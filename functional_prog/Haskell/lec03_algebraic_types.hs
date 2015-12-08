type Symbol = Char
type ListOfIntegers = [Integer]
type PartOfDoubles = (Double, Double)
type IntegerFn = Integer -> Integer
type PolymorficFn a = a -> a
type Optional = Maybe Integer

type String = [Char]
type FilePath = [Path]

-----
������ ������: �������������� ����

data Bool = False | True
	��� ����  ������������ �������� ����
data Int = ����. ����.|...|...|-2|-1|0|1|2|...| ����. ����

-----
data Rainbow = Red | Orange | Yellow | Green | Cyan | Blue | Violet
	deriving(Show, Read, Enum, Ord, Eq)

����� Rainbow ������������� � String ���� ����� �� ��� �� Show(����� ����� show - ������� � ������)
����� ������� ���� ��� ���������� �������������� String -> Rainbow, ��� ����� Rainbow ������ ������������ � Read
[Orange .. Blue]
���������
succ Red
pred Orange
Yellow > Red
Blue /= Orange
print Red
(read "Cyan")::Rainbow
-----
���������� foldr
-----

class Eq a where
	(==) :: a -> a -> Bool
	(/=) :: a -> a -> Bool
	x == y = not (x/=y)
	
class (Eq a) => Ord a where
	(>), (<), (<=), (>=), :: a -> a -> Bool
	min, max :: a -> a -> a
-----
Functor
	fmap
:i Functor

fmap words getline
ab cd ef ...
-----
���������� ������ �������
����������� ������� ���������� ������ eq ��� ��������, ��� ��������� �� �� ��������� ��� �����������
����������� ����������� ��� ��� ����� ��� ���������� ������ � ��������� ��� � ������� Bool
Bool	\
		| Logic
Ternary /	