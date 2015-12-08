-- fs2hs-lib.hs utf8 ru unix eolns

nop xs = xs
push x xs = x:xs

-- f :: Stack -> m Stack

add  (x2:x1:xs) = (x1 + x2):xs
sub  (x2:x1:xs) = (x1 - x2):xs
mul  (x2:x1:xs) = (x1 * x2):xs
div' (x2:x1:xs) = (x1 `div` x2):xs
mod' (x2:x1:xs) = (x1 `mod` x2):xs

lt (x2:x1:xs) = bool2int (x1 < x2) : xs
gt (x2:x1:xs) = bool2int (x1 >  x2) : xs
le (x2:x1:xs) = bool2int (x1 <=  x2) : xs
ge (x2:x1:xs) = bool2int (x1 >= x2) : xs
eq (x2:x1:xs) = bool2int (x1 == x2) : xs
ne (x2:x1:xs) = bool2int (x1 /= x2) : xs

or'  (x2:x1:xs) = (abs x1 + abs x2):xs
and' (x2:x1:xs) = (x1 * x2):xs

not' (0:xs) = (1:xs)
not' (_:xs) = (0:xs)

dup   (x:xs) = (x:x:xs) 
drop' (x:xs) = xs

swap (x2:x1:xs) = (x1:x2:xs)
over (x2:x1:xs) = (x1:x2:x1:xs)

rot (x3:x2:x1:xs) = (x1:x3:x2:xs)

dup2  (x2:x1:xs) = (x2:x1:x2:x1:xs)
over2 (x4:x3:x2:x1:xs) = (x2:x1:x3:x3:x2:x1:xs)

-- f :: Stack -> Stack -- flow ctrl --

ifThen fn (flag:xs)
    | flag /= 0 = fn xs
    | otherwise = xs

{-  
doLoop fn (from:upto:xs) = doLoop' fn from upto xs

doLoop' fn from upto xs
    | from < upto = doLoop' fn (from+1) upto (fn xs)
    | otherwise = xs
    
-}  {-  testloop = doLoop ( add . push 1 . dup ) . push 1 . push 5 . push 1
        > testloop []
        [5,4,3,2,1]
        : testloop 1 5 1 do dup 1 + loop ;
    -}   
    
doLoop fn (from:upto:xs) = doLoop' fn from upto xs

doLoop' fn from upto xs
    | from < upto = doLoop' fn (from+1) upto (fn from xs)
    | otherwise = xs

{-  doLoop is ok with index !!!

    gforth:
    
    : testloop1 5 1 do I 1 + loop ; redefined testloop1   ok
    testloop1  ok
    .s <4> 2 3 4 5  ok  
    
    fs2hs -> ghci:
    
    testloop1 = doLoop (\ i -> add . push 1 . push i ) . push 1 . push 5
    >testloop1 []
    [5,4,3,2]
-}

--  +loop
--  в момент рекурсивного вызова (если делать как в loop)
--  приращения в стеке ещё нет! 
-- (фактически имеет место замена цикла с постусловием на цикл с предусловием)

doLoopPlus fn (from:upto:xs) = doLoopPlus' fn from upto (fn from xs)

doLoopPlus' fn from upto (step:xs)
    | from' < upto = doLoopPlus' fn from' upto (fn from' xs)
    | otherwise = xs
    where
        from' = from + step

-- until' :: ( [Int] -> [Int] ) -> [Int] -> [Int]

until' fn xs = until1 fn (fn xs)

until1 fn (x:xs)
    | x == 0 = until1 fn (fn xs)
    | otherwise = xs
        
-- f :: Stack -> IO Stack -- functions with side effects --

dot :: [Int] -> IO [Int]
dot (x:xs) = putStr (show x) >> putStr " " >> return xs

cr :: [Int] -> IO [Int]
cr xs = putStrLn "" >> return xs

-- utils --

bool2int True  = -1
bool2int False =  0

-- eof
