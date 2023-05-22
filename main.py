import math
import random
from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, error, S):
        b = round(-math.log(error)/(math.log(2)**2))
        self.n = S * b
        self.S = S
        self.data = bitarray(self.n)
        self.data.setall(0)
        self.k = round(b * math.log(2))
        self.hash = []
        for _ in range(self.k):
            a = [random.randint(1, self.n) for _ in range(4)]
            self.hash.append(lambda x: sum([x[i] * a[i] for i in range(4)]) % self.n)

    def insert(self, v):
        for h in self.hash:
            self.data[h(v)] = 1

    def lookup(self, v):
        for h in self.hash:
            if self.data[h(v)] == 0:
                return False
        return True

def rand_ip():
    return tuple(random.randint(0, 255) for _ in range(4))



size = 10000
filter = BloomFilter(error=0.001, S=size)
ips = set()
for _ in range(size):
    ip = rand_ip()
    ips.add(ip)
    filter.insert(ip)

k = 0
n = 0
for _ in range(size):
    ip = rand_ip()
    if ip not in ips:
        n += 1
        if filter.lookup(ip):
            k += 1
print(k/n)
