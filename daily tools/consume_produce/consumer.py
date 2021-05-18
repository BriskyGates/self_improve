import time
from threading import Thread, currentThread


class ConsumerThread(Thread):
    def __init__(self, tname, kiwi, condition):
        Thread.__init__(self, name=tname)
        self.kiwi = kiwi
        self.condition = condition

    def run(self):
        while True:
            self.condition.acquire()
            if self.kiwi.count > 0:
                time.sleep(1)
                self.kiwi.consume()
                print(currentThread().name + "消费一个面包,当前面包量:" + str(self.kiwi.count))
                self.condition.release()
            else:
                print(currentThread().name + "没面包了,赶紧生产!")
                self.condition.notifyAll()  # 唤醒condition对象中等待的生产线程
                self.condition.wait()


"""

注释掉条件判断中的notifyall,第一个可以提醒到生产线程, 而后无法提醒到,我觉得是主线程安排的

"""
