root (a, b, c) 
      | d < 0 = []
      | a == 0 = [-b/c]
      | d == 0 = [(-b)/2*c]
      | otherwise = [(-b+sqrt(d))/(2*a), (-b-sqrt(d))/(2*a)]
  where d = b^2 - 4*a*c