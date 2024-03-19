#Fatih Gümüş
F = GF(1073741789)
E = EllipticCurve(F, [382183198, 410736703])
G = E((431583365, 858920426))
r = 1073759053

a = randint(2, r-2)
b = randint(2, r-2)

A = a * G
B = b * G

S_A = a * B
S_B = b * A

print("Secret key of A:", S_A)
print("Secret key of B:", S_B)