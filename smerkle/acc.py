"""Main Library for Pyproofs"""
import hashlib
import math

from Crypto.Util import number

def get_prime(digits=512, strong=True):
    if strong:
        return number.getStrongPrime(digits)
    else:
        return number.getPrime(digits)

# Cryptographic Accumulators

def mod_exp(a, b, n):
    """
    Returns the result of
    (a ^ b) mod n
    """
    result = 1
    while True:
        if b % 2 == 1:
            result = (a * result) % n

        b = b / 2

        if b == 0:
            break

        a = (a * a) % n

    return result


def increment_membership_accumulator(acc, value, n):
    return mod_exp(acc, value, n)


def verify_hash_membership(acc, value, witness, n):
    expected_acc = increment_membership_accumulator(witness, value, n)
    return acc == expected_acc


def add_many_memberships(acc, values, n):
    witnesses = {}
    u = acc
    cumulative_witnesses = []
    reverse_cumulative_witnesses = []

    asc_acc = acc
    desc_acc = acc
    for i in range(len(values)):
        my_witness = acc
        for j in range(len(values)): # inefficient
            if i == j:
                continue
            else:
                my_witness = increment_membership_accumulator(my_witness, values[j], n)
        witnesses[values[i]] = my_witness
        u = increment_membership_accumulator(u, values[i], n)

    for value in witnesses:
        assert verify_hash_membership(u, value, witnesses[value], n)

    return u, witnesses


def compute_non_membership_witness(acc, value, g, n, values):
    # WIP, CURRENTLY BROKEN
    
    # https://www.cs.purdue.edu/homes/ninghui/papers/accumulator_acns07.pdf
    
    # u = multiple of all values in set
    # all values are primes
    # non-member value is X
    # gcd(x, u) == 1
    # thus there exists some ax + bu = 1
    # let a2 = a + kx and let b2 = b + ku
    # then a2 * u + b2 * x = 1
    # let d = g ^ -b2 mod n
    # nonmembership witness is (a, d)
    # let c = g^u = our membership accumulator value
    # separately we have
    # (c^a = g^(u*a) = g^(1-bx) = g^(-bx) * g = d^x * g ) mod n
    # if above is true with given witness (a, d), nonmembership is true
    # to verify just show that c^a mod n == d^x * g mod n

    assert not value in values
    
    u = 1
    for x in values:
        u = u * x

    gcd, a, b = xgcd(value, u)
    assert gcd == 1
    if a < 0:
        a_diff = -a / u + 1
    else:
        a_diff = 0
    if b > 0:
        b_diff = b / value + 1
    else:
        b_diff = 0
    k = max(a_diff, b_diff)
    a2 = a + k * u
    b2 = b - k * value
    
    try:
        assert b2 > 0
        assert a2 > 0
    except:
        import pdb;pdb.set_trace()
    try:
        assert a2 * value + b2 * u == 1
    except:
        import pdb;pdb.set_trace()
    assert a * value + b * u == 1

    d = mod_inverse(mod_exp(g, b2, n), n)
   # import pdb;pdb.set_trace()
    assert verify_non_membership(acc, a2, d, value, g, n)
    return a2, d

def verify_non_membership_old(acc, witness_a, witness_d, value, g, n):
    left = mod_exp(acc, witness_a, n)
    right = (mod_exp(witness_d, value, n) * (g % n)) % n
    import pdb;pdb.set_trace()
    return left == right

    

def xgcd(b, n):
    """
    Performs Extended Euclidian Algorithm.
    Returns GCD(X, Y), A, B for equation
    X*A + Y*B = GCD(X, Y) where X, Y, A, B are all integers.
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def mod_inverse(a, n):
    # ax + by = gcd(a, b)
    # a * x mod b = 1
    # b * y mod a = 1
    #
    # mod_inverse(a) * a mod n = 1

    # solve for X where a=a and b=n
    gcd, x, y = xgcd(a, n)
    assert gcd == 1 # this only works for coprime numbers
    return x