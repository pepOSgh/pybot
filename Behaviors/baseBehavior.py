__author__ = 'pepOS'


class BaseBehavior:
    def __init__(self, factory):
        self.factory = factory

    def run_algorithm(self):
        assert 0, 'action must be defined!!'
