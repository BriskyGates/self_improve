import time
from threading import Thread, currentThread

MAX_KIWI = 5  # 仓库最大库存量


class ProducerThread(Thread):
    def __init__(self, producer, kiwi, condition):
        Thread.__init__(self, name=producer)
        self.kiwi = kiwi  # 保证数据共享
        self.condition = condition

    def run(self):
        while True:
            self.condition.acquire()  # 添加condition对象的锁
            if self.kiwi.count < MAX_KIWI: # 下标从0开始,所以生产到第四个就停止了,即<5
                time.sleep(1)  # 不释放锁
                self.kiwi.produce()  # 生产和消费是互斥
                print(currentThread().name + "生产一个面包,当前面包数量:" + str(self.kiwi.count))
                # self.condition.notifyAll()  # 唤醒self.condition中的等待的消费线程,有消费在等待,无等待线程,也不会出错
                self.condition.release()
            else:
                print(currentThread().name + "库存已满,停止生产")
                # self.condition.notifyAll()
                self.condition.wait()  # 挂起当前生产线程,并释放CPU和锁,并不能通知等待线程


"""
两个判断语句中的notifyall 全部注释后无法通知等待的消费线程,只是挂起当前的线程

分析:
两个生产者线程先后获取锁,发现库存已满,先提醒等待中的消费线程, 然后将当前线程挂起

self.condition.notifyAll()
self.condition.wait()  # 挂起当前生产线程,并释放CPU和锁

"""
