# Fatih Gümüş

p = 16777213
F = GF(p)
a = F(2914938)
b = F(16233063)
E = EllipticCurve([a,b])
n = 16781623
G = E((11659968 , 12337680))
P = E((16440277 , 6760834))
k = 10
Cl = []
Dl = []
Rl = []
for i in range (k):
    c = randint(2,n-1)
    d = randint(2,n-1)
    R = c*G + d*P
    Cl.append(c)
    Dl.append(d)
    Rl.append(R)
a = randint(2,n-1)
b = randint(2,n-1)
a1 = a
b1 = b

T = a*G + b*P
S = a1*G + b1*P

Z = Integers()
counter = 0
while(True):
    s1 = Z(S[0]) % k
    S = S + Rl[s1]
    a1 = (a1 + Cl[s1]) % n
    b1 = (b1 + Dl[s1]) % n
    s1 = Z(S[0]) % k
    S = S + Rl[s1]
    a1 = (a1 + Cl[s1]) % n
    b1 = (b1 + Dl[s1]) % n
    s1 = Z(T[0]) % k
    T = T + Rl[s1]
    a = (a + Cl[s1]) % n
    b = (b + Dl[s1]) % n
    counter = counter + 1
    if T == S or T == -S:
        break

if b == b1:
    print("Error: division by zero")
else:
    if T == -S:
        alpha1 = inverse_mod((b + b1), n)
        alpha = ((a1 + a)*alpha1) % n
    else:
        alpha1 = inverse_mod((b - b1), n)
        alpha = ((a1 - a)*alpha1) % n
print(alpha,counter)
