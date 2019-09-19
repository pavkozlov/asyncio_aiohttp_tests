def subgen():
    x = 'Ready to accept message'
    message = yield x
    print(f'Subgen received: {message}')


def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


class BlaBlaExc(Exception):
    pass

@coroutine
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done')
        except BlaBlaExc:
            print('..................')
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)
