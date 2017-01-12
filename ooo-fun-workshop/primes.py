from memory_profiler import profile


def is_prime(number):
    divisible = False

    for i in range(2, number):
        if number % i == 0:
            divisible = True
            break

    return number > 1 and not divisible


def is_prime_fun(number):
    return number > 1 \
        and not any(filter(lambda i: number % i == 0, range(2, number)))


if __name__ == "__main__":
    @profile
    def primes():
        return list(i for i in range(1, 10000) if is_prime(i))

    primes = primes()

    @profile
    def primes_fun():
        return list(i for i in range(1, 10000) if is_prime_fun(i))

    primes_fun = primes_fun()
