from abc import ABC, abstractmethod
from hero import *


class AbstractEffect(Hero, ABC):

    def __init__(self, base):
        self.base = base


class AbstractPositive(AbstractEffect):
    def get_positive_effects(self):
        self.base.get_positive_effects()


class AbstractNegative(AbstractEffect):

    @abstractmethod
    def get_negative_effects(self):
        pass


    
class Berserk(AbstractPositive):

    self.base.stats

class Blessing(AbstractPositive):
    pass


class Weakness(AbstractNegative):
    pass


class Curse(AbstractNegative):
    pass


class Evileye(AbstractNegative):
    pass
