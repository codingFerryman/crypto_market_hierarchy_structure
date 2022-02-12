from functools import lru_cache

from libparser.parser import Parser


@lru_cache
def get_parser():
    return Parser()


def parse(stmt: str):
    return get_parser().parse(stmt)
