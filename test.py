load math2

x:int = 30
print(math2.add(20, x))
print(x)

def main()->"None":
    print("390")

def fib(n:int)->"int":
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

e:int = fib(20)

print(e)

