from typing import List


def maximum(arr):
    if not arr:
        raise ValueError('Cannot find maximum in an empty list')

    if len(arr) == 1:
        return arr[0]

    x, *tail = arr
    max_tail = maximum(tail)
    return x if x > max_tail else max_tail


def minimum(arr: List[int]) -> int:
    x, *tail = arr
    if not tail:
        return x

    return min(x, minimum(tail))


def replicate(n, val):
    if n <= 0:
        return []

    return [val, *replicate(n-1, val)]


def take(n, arr):
    if n <= 0 or not arr:
        return []

    x, *tail = arr
    return [x, *take(n-1, tail)]


def reverse(arr):
    if not arr:
        return []

    x, *tail = arr
    return [*reverse(tail), x]


def zip(xs, ys):
    if not xs or not ys:
        return []

    x, *x_tail = xs
    y, *y_tail = ys
    return [(x, y), *zip(x_tail, y_tail)]


def elem(val, arr) -> bool:
    if not arr:
        return False

    x, *tail = arr
    if val == x:
        return True
    return elem(val, tail)


def fib(n: int) -> int:
    if n == 0 or n == 1:
        return n

    return fib(n-2) + fib(n-1)


def quicksort(arr):
    if not arr:
        return []
    x, *tail = arr
    smaller_sorted = quicksort([t for t in tail if t <= x])
    bigger_sorted = quicksort([t for t in tail if t > x])
    return [*smaller_sorted, x, *bigger_sorted]


if __name__ == '__main__':
    arr = [7, 1, 2, 4, 5, 9, 3]
    print(f'Max of list {arr} is {maximum(arr)}')
    print(f'Min of list {arr} is {minimum(arr)}')

    print(replicate(3, 42))
    print(take(3, [0, 1, 2, 3, 4]))
    print(take(3, []))

    print(reverse([1, 2, 3, 4, 5]))
    print(reverse([]))

    arr1 = [1, 2, 3]
    arr2 = ['a', 'b', 'c', 'd']
    print(zip(arr1, arr2))

    print(elem(0, arr1))
    print(elem('d', arr2))
    print(f'fib(7) = {fib(7)}')

    print(f'Sorted {arr} is {quicksort(arr)}')
