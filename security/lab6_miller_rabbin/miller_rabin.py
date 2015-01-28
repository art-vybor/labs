import random

# http://rosettacode.org/wiki/Miller-Rabin_primality_test
# http://ru.numberempire.com/primenumbers.php

def is_prime(n, k=5):
    if n == 2:
        return True
    elif n > 2:        
        if n % 2 == 0: return False

        # try to found s, t: n-1 == 2**s * t, and t is odd
        s = 0
        t = n-1
        while t%2 != 1:
            s += 1
            t /= 2
     
        for _ in range(k):
            a = random.randrange(2, n)

            x = pow(a, t, n)
            if x == 1 or x == n-1: continue

            f = False
            for _ in range(s-1):
                x = pow(x, 2, n)
                if x == 1: return False
                if x == n - 1: 
                    f = True
                    break                    
            if not f: return False 
        return True

a1, a2 = map(int, raw_input().split())

while not is_prime(a1):
    a1 += 1
print a1, 

n = a2
a2 = 4
while not is_prime(a2):
    a2 = random.randrange(2**(n-1)+1, 2**n, 2)
print a2


# # test
# print is_prime(2)
# print is_prime(3)
# print is_prime(4)
# print is_prime(5)
# print is_prime(643808006803554439230129854961492699151386107534013432918073439524138264842370630061369715394739134090922937332590384720397133335969549256322620979036686633213903952966175107096769180017646161851573147596390153)
# print is_prime(743808006803554439230129854961492699151386107534013432918073439524138264842370630061369715394739134090922937332590384720397133335969549256322620979036686633213903952966175107096769180017646161851573147596390153)
# print is_prime(666278359389517568216534080393)
# print is_prime(1008704736637390313513101213337497368610966677496731131686771)
# print is_prime(935191495292858362821108067845913270550002172350761814478365379232516074389106599458627833)
# print is_prime(918186947498536286096183527288503522930953965709345494078094989849497165602384449590520296583670761522260227667651713357)
