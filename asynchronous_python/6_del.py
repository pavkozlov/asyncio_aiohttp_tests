def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


class BlaBlaExc(Exception):
    pass


def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print('...', message)
    return 'Returned from subgen'


@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except BlaBlaExc as e:
    #         g.throw(e)
    result = yield from g
    print(result)
