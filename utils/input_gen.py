def get(*args):
    for query in args:
        data = input(query)
        yield data if data != '' else None
