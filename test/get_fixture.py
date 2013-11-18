from os import path

fixtures_dir = path.join(path.dirname(path.realpath(__file__)), 'fixtures')

def get_fixture(name):
    return path.join(fixtures_dir, name)
