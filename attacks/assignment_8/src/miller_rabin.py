import secrets


def miller_rabin(n, rounds=20):
    if n < 2:
        return False, 0, []

    if n == 2 or n == 3:
        return True, 0, []

    if n % 2 == 0:
        return False, 0, []

    d = n - 1
    s = 0

    while d % 2 == 0:
        d //= 2
        s += 1

    bases = []

    for i in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        bases.append(a)

        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        passed = False

        for j in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                passed = True
                break

        if not passed:
            return False, i + 1, bases

    return True, rounds, bases


if __name__ == "__main__":
    number = 101

    result, used_rounds, bases = miller_rabin(number)

    print("Number:", number)
    print("Probable prime:", result)
    print("Rounds executed:", used_rounds)
    print("Bases:", bases)
