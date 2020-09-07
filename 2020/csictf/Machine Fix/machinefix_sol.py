def count3(n):
    sum = 0
    while (n > 0):
        sum += n
        n //= 3
    return sum

print(count3(50))
print(count3(523693))
print(count3(523693181734689806809285195318))
