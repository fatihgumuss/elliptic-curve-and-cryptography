#Fatih Gümüş
F = GF(1073741789)
E = EllipticCurve(F, [382183198, 410736703])
G = E((431583365, 858920426))
r = 1073759053

k = randint(2, r-2)
Q = k * G

print("k:", k)
print("Q:", Q)

message = randint(2, r-2)
print("message:", message)

d = randint(2, r-2)
print("d:", d)

X = d * G
print("[d]G:", X)

x1 = X[0]
x1_prime = int(x1)

t = x1_prime % r
print("t:",t)

e = hash(message)
print("e:", e)

s = inverse_mod(d, r) * (e + k * t) % r
print("s:", s)
print("(t, s):", (t, s))

w = inverse_mod(s, r)
print("w:", w)
u1 = (e * w) % r
print("u1:", u1)
u2 = (t * w) % r
print("u2:", u2)

X = u1 * G + u2 * Q
print("X:", X)

if X.is_zero():
    print("Reject the signature")
else:
    x1 = X[0]
    x1_prime = int(x1)
    v = x1_prime % r
    print("v:", v)
    if v == t:
        print("Accept the signature")
    else:
        print("Reject the signature")