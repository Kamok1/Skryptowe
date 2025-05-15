from __future__ import annotations

import functools
import logging
import random
import string
import time
from functools import lru_cache
from itertools import dropwhile, accumulate, repeat, islice
from typing import Callable, Generator, Iterable, Iterator, Sequence, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def acronym(words: Iterable[str]) -> str:
    return "".join(w[0].upper() for w in words if w)


def median(numbers: Sequence[float]) -> float:
    nums = sorted(numbers)
    mid = len(nums) // 2
    return sum(nums[mid - 1:mid + 1]) / (2 - len(nums) % 2)

def root(x: float, epsilon: float = 1e-10) -> float:
    start = x if x > 1 else 1.0
    approximations = accumulate(
        repeat(0),
        lambda y, _ : (y + x / y) / 2,
        initial=start
    )
    return next(dropwhile(
        lambda y: abs(y * y - x) > epsilon,
        approximations
    ))

def make_alpha_dict(text: str) -> dict[str, list[str]]:
    words = text.split()
    letters = set(c for word in words for c in word if c.isalpha())
    return { ch: [word for word in words if ch in word]  for ch in sorted(letters) }



def flatten(seq):
    return [x for el in seq for x in (flatten(el) if isinstance(el, (list, tuple)) else [el])]


def forall(pred, iterable):
    for x in iterable:
        if not pred(x):
            return False
    return True

def exists(pred, iterable):
    for x in iterable:
        if pred(x):
            return True
    return False

def atleast(n, pred, iterable):
    seq = list(iterable)
    seq_len = len(seq)
    count = 0
    for i, x in enumerate(seq):
        count += pred(x)
        if count >= n:
            return True
        if seq_len - (i + 1) < n - count:
            return False
    return False


def atmost(n, pred, iterable):
    count = 0
    for x in iterable:
        count += pred(x)
        if count > n:
            return False
    return True


DEFAULT_CHARSET: str = string.ascii_letters + string.digits


class PasswordGenerator(Iterator[str]):
    def __init__(self, length: int, charset: str = DEFAULT_CHARSET, count: int = 1000):
        if length <= 0:
            raise ValueError("length must be positive")
        if count <= 0:
            raise ValueError("count must be positive")
        self.length = length
        self.charset = charset
        self.count = count
        self._generated = 0

    def __iter__(self) -> PasswordGenerator:
        return self

    def __next__(self) -> str:
        if self._generated >= self.count:
            raise StopIteration
        self._generated += 1
        return "".join(random.choices(self.charset, k=self.length))



def make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1
    return generator()


@lru_cache(maxsize=None)
def make_generator_mem(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    return make_generator(f)


def log(level: int = logging.INFO):
    def decorator(obj):
        if isinstance(obj, type):
            original_init = obj.__init__
            def new_init(self, *args, **kwargs):
                logging.log(level, f"Instancja klasy {obj.__name__} args={args} kwargs={kwargs}")
                original_init(self, *args, **kwargs)
            obj.__init__ = new_init
            return obj
        else:
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = obj(*args, **kwargs)
                duration = time.perf_counter() - start
                logging.log(
                    level,
                    f"Funkcja {obj.__name__} wywołana z args={args}, kwargs={kwargs}, wynik={result}, czas={duration:.6f}s"
                )
                return result
            return wrapper
    return decorator     m

if __name__ == "__main__":
    print("acronym:", acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))
    print("median:", median([1, 3, 2, 4]))
    print("pierwiastek:", root(3, epsilon=0.1))
    print("make_alpha_dict:", make_alpha_dict("on i ona"))
    print("flatten:", flatten([1, [2, 3], [[4, 5], 6]]))

    is_even = lambda x: x % 2 == 0
    print("forall parzyste (0‑6):", forall(is_even, range(0, 7)))
    print("exists parzyste (0‑5):", exists(is_even, range(0, 5)))
    print("atleast 3 patrzyse (0‑10):", atleast(3, is_even, range(0, 11)))
    print("atmost 1 parzyste (1,3,5):", atmost(1, is_even, [1, 3, 5]))

    pg = PasswordGenerator(length=8, count=3)
    for pwd in pg:
        print("password:", pwd)
    pg = PasswordGenerator(length=50, count=1)
    print("password:", pg.__next__())


    square = lambda n: n * n
    gen = make_generator(square)
    print("pierwsze 5 kwadratów:", list(islice(gen, 5)))


    def fib(n: int) -> int:
        if n < 2:
            return n
        return fib(n - 1) + fib(n - 2)


    print("pierwsze 15 fib:", list(islice(make_generator_mem(fib), 15)))

    start = time.perf_counter()
    result2 = list(islice(make_generator(fib), 15))
    t2 = time.perf_counter() - start
    print(f"[bez memoizacji] czas: {t2:.6f}s")


    start = time.perf_counter()
    result1 = list(islice(make_generator_mem(fib), 100))
    t1 = time.perf_counter() - start
    print(f"[memoizacja] czas: {t1:.6f}s")



    @log(logging.DEBUG)
    def add(a, b):
        return a + b

    add(2, 3)

    @log()
    class Test:
        def __init__(self, x):
            self.x = x

    Test(42)
