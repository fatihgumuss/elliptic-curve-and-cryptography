#Fatih Gümüş
from sage.all import *
import hashlib
import hmac
import binascii

F = GF(1073741789)
E = EllipticCurve(F, [382183198, 410736703])
G = E((431583365, 858920426))
r = 1073759053
h = 1

def compute_R_prime(R):
    f = int(floor(log(r, 2)) + 1)
    x_prime = Integer(R[0]) % (2 ^ f/2)
    return x_prime

def KDF(xZ):
    xZ_str = str(xZ)
    xZ_bytes = xZ_str.encode()
    hash_val = hashlib.sha3_512(xZ_bytes).digest()
    k1 = hash_val[:len(hash_val) // 2]
    k2 = hash_val[len(hash_val) // 2:]
    return k1, k2

def MAC(key, *data):
    data_str = ''.join(str(d) for d in data)
    data_bytes = data_str.encode()
    h = hmac.new(key, data_bytes, hashlib.sha3_512)
    return h.hexdigest()
print("User A picks kA,dA and does the calculations ")
kA = randint(2, r - 2)
print("kA = ",kA)
QA = kA * G
print("QA = ",QA)
A = "Alice"
print("A  = ",A)
dA = randint(2, r - 2)
print("dA = ",dA)
RA = dA * G
print("RA = ",RA)
print("A sends A and RA")

print("\nUser B picks kB,dB and calculates the needing parameters")
kB = randint(2, r - 2)
print("kB = ",kB)
QB = kB * G
print("QB = ",QB)
B = "Bob"
print("B  = ",B)
dB = randint(2, r - 2)
print("dB = ",dB)
RB = dB * G
print("RB = ",RB)
R_prime_B = compute_R_prime(RB)
print("R_prime_B = ",R_prime_B)
sB = (dB + int(R_prime_B) * kB) % r
print("sB = ",sB)
R_prime_A = compute_R_prime(RA)
print("R_prime_A = ",R_prime_A)
ZB = h * sB * (RA + int(R_prime_A) * QA)
print("ZB = ",ZB)
if ZB.is_zero():
        print("Error: ZB is equal to infinity")
        exit()
k1, k2 = KDF(ZB[0])
print("k1 = ",k1)
print("k2 = ",k2)
tB = MAC(k1, 2, B, A, RB, RA)
print("tB = ",tB)
print("B sends B,RB,tB")

print("\nUser A do the calculations with received parameters and check if t = tB")
R_prime_A = compute_R_prime(RA)
print("R_prime_A = ",R_prime_A)
sA = (dA + int(R_prime_A) * kA) % r
print("sA = ",sA)
R_prime_B = compute_R_prime(RB)
print("R_prime_B = ",R_prime_B)
ZA = h * sA * (RB + int(R_prime_B) * QB)
if ZA.is_zero():
        print("Error: ZA is equal to infinity")
        exit()
print("ZA = ",ZA)
k1, k2 = KDF(ZA[0])
print("k1 = ",k1)
print("k2 = ",k2)
t = MAC(k1, 2, B, A, RB, RA)
print("t  = ",t)
if t != tB:
    print("Error: t != tB")
    exit()
else:
    tA = MAC(k1, 3, A, B, RA, RB)
    print("tA = ",tA)
    print("A sends tA")
    print("B computes t and check if t = tA")
    t = MAC(k1, 3, A, B, RA, RB)
    print("t  =",t)
    if t != tA:
        print("Error: t != tA")
        exit()
        
    else:
        session_key = k2
        print("Protocol run successful.")
        print("Session key:", session_key)