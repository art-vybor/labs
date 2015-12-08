type Symbol = Char
type ListOfIntegers = [Integer]
type PartOfDoubles = (Double, Double)
type IntegerFn = Integer -> Integer
type PolymorficFn a = a -> a
type Optional = Maybe Integer

type String = [Char]
type FilePath = [Path]

-----
Вторая группа: алгебраические типы

data Bool = False | True
	имя типа  конструкторы значений типа
data Int = наим. знач.|...|...|-2|-1|0|1|2|...| макс. знач

-----
data Rainbow = Red | Orange | Yellow | Green | Cyan | Blue | Violet
	deriving(Show, Read, Enum, Ord, Eq)

чтобы Rainbow преобразовать к String надо чтобы он был из Show(чтобы юзать show - перевод в строку)
Чтобы считать этот тип необходимо преобразование String -> Rainbow, для этого Rainbow должен принадлежать к Read
[Orange .. Blue]
сравнение
succ Red
pred Orange
Yellow > Red
Blue /= Orange
print Red
(read "Cyan")::Rainbow
-----
посмотреть foldr
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
допиливать старые задания
попробовать создать воплощение класса eq для деревьев, для сравнения их на равенство или неравенство
разработать собственный тип или класс для трёхзначной логики и подружить его с классом Bool
Bool	\
		| Logic
Ternary /	