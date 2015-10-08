gcd' a b = if b == 0 then a else gcd' b (rem a b)
lcm' :: Integral a => a -> a -> a
lcm' a b = abs( (quot a (gcd' a b)) * b )
 