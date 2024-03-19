#Fatih Gümüş
F = GF(1073741789)
E = EllipticCurve(F, [382183198, 410736703])
G = E((431583365, 858920426))
r = 1073759053

xa = randint(1, r-2)
xb = randint(1, r-2)
xc = randint(1, r-2)

Ka = xa*G
Kb = xb*G
Kc = xc*G

Ka_to_B = Ka
Kb_to_A = Kb
Kb_to_C = Kb
Kc_to_B = Kc

Kab = xb*Ka_to_B
Kbc = xc*Kb_to_C
Kca = xa*Kc_to_B

Kca_to_B = Kca
Kab_to_A = Kab
Kbc_to_C = Kbc

K = xa*Kbc_to_C
print(K)
K = xc*Kab_to_A
print(K)
K = xb*Kca_to_B
print(K)