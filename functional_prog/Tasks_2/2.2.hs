fib n 
    |n == 0 = 0
    |n == 1 = 1
    |otherwise = fib (n-1) + fib (n-2)
    
fib1 m n = [fib x | x <- [m..m+n-1]]