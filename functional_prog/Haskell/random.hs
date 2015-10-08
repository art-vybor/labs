import System.Random
 
main = do
   gen <- newStdGen
   let ns = randoms gen :: [Int]
   let bs = randoms gen :: [Bool]
   print $ take 3 ns
   print $ take 2 bs
   
   