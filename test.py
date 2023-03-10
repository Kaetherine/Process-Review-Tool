n = 10
i = n
j = 1
k = 0


def test():
    global i, j, k
    while i > 0:
        while j < n:
            while k < j:
                e = 1 + 2
                print(e)
                k = k + 1
            j = 2 * j
        i = i - 1
    return {i, j, k}

test()
