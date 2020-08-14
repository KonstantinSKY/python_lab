class Value:
    def __init__(self):
        self.amount = 0
        self.commission = 0

    def __get__(self, instance, owner):
        return self.amount

    def __set__(self, instance, value):
        self.amount = value - value * instance.commission


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
