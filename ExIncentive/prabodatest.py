a = [1,3,5,6,7,8,9,10]
odd = 0
eve = 0
for no in a:
    if no % 2 == 0:
        eve = eve +1
    else:
        odd = odd +1
print("Even No Count "+str(eve))
print("Odd No Count "+str(odd))


print("###################")

print("Numbers which are divisible by 7 and multiple of 5 are")
for n in range(1500, 2800):
    if n % 5 == 0:
        if n % 7 == 0:
            print(str(n))
