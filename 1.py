def f(n):
    b = bin(n)[2::]
    if len(b) % 2 == 0:
        b = b[0:3] + '1' + b[3::]
    if int(b, 2) >= 26:
        return n
    else:
        return 10000000

sp = []
for e in range(1000):
    sp.append(f(e))
print(min(sp))
