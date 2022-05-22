a = 10


def fun():
    global a
    # a = 20
    a = a + 30


fun()

print(a)
