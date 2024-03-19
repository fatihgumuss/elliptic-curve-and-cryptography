#Fatih Gümüş
from sage.crypto.block_cipher.des import DES
import hashlib
import hmac

F = GF(1073741789)
E = EllipticCurve(F, [382183198, 410736703])
G = E((431583365, 858920426))
r = 1073759053
h = 1

def KDF(xZ, R):
    xZ_str = str(xZ)
    xZ_bytes = xZ_str.encode()
    hash_val = hashlib.sha3_512(xZ_bytes).digest()
    k1 = hash_val[:8].hex()  # First 8 bytes (64 bits) as hex
    k2 = hash_val[8:].hex()  # Remaining bytes as hex
    return k1, k2

def MAC(key, *data):
    data_str = ''.join(str(d) for d in data)
    data_bytes = data_str.encode()
    key_bytes = bytes.fromhex(key)
    h = hmac.new(key_bytes, data_bytes, hashlib.sha3_512)
    return h.hexdigest()

def ECIES_encrypt(Q, m):
    print("User A picks a random d,make the calculations and check if Z is infinity or not")
    while True:
        d = randint(2, r - 2)
        print("d = ",d)
        R = d * G
        print("R = ",R)
        Z = h * d * Q
        print("Z = ",Z)
        if not Z.is_zero():
            break
    xZ = Z.xy()[0]
    print("User A calculates k1,k2 and encrypts the plaintext")
    k1, k2 = KDF(xZ, R)
    print("User A calculates k1 and k2")
    print("k1 =",k1)
    print("k2 =",k2)
    des = DES()
    k1 = "0x"+k1
    C = des.encrypt(plaintext=m, key=k1)
    print("C  =",C.hex())
    t = MAC(k2, C)
    print("t  =",t)
    print("User A sends R,C and t to User B")
    return R, C, t

def ECIES_decrypt(k, ciphertext):
    R, C, t = ciphertext
    print("User B checks if the R is valid and Z is not infinity")
    if R.is_zero():
        return 'Reject the ciphertext'
    Z = h * k * R
    print("Z  =",Z)
    if Z.is_zero():
        return 'Reject the ciphertext'
    xZ = Z.xy()[0]
    k1, k2 = KDF(xZ, R)
    print("User B calculates the needed parameters and checks if t' = t")
    print("k1 =",k1)
    print("k2 =",k2)
    t_prime = MAC(k2, C)
    print("t' =",t_prime)
    if t_prime != t:
        return 'Reject the ciphertext'
    des = DES()
    print("User B decrypts the message")
    m = des.decrypt(ciphertext=C, key=int(k1, 16))
    print("Decrypted message  :","0x"+m.hex())

# Example usage
plaintext = 0x01A1D6D039776742
print("Picked plaintext :","0x"+plaintext.hex())
k = randint(2,r-2)
print("Private key of User B :",k)
Q = k*G
print("Public key of User A :",Q)
# Encryption
ciphertext = ECIES_encrypt(Q, plaintext)
# Decryption
ECIES_decrypt(k, ciphertext)