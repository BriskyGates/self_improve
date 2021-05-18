class Kiwi:
    """用来生产猕猴桃和消耗猕猴桃"""
    def __init__(self):
        self.count = 0

    def produce(self):  # 生产猕猴桃
        self.count += 1

    def consume(self):
        self.count -= 1
