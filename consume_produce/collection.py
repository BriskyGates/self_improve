from threading import Condition

from consume_produce.consumer import ConsumerThread
from consume_produce.goods import Kiwi
from consume_produce.producer import ProducerThread

if __name__ == "__main__":
    kiwi = Kiwi()
    conn = Condition()

    for i in range(2):  # 两个生产者
        pro = ProducerThread("生产者" + str(i), kiwi, conn)
        pro.start()
    for j in range(1, 2):  # 一个消费者
        consumer = ConsumerThread("消费者" + str(j), kiwi, conn)
        consumer.start()
    # for i in range(2):  # 两个生产者
    #     pro = ProducerThread("生产者" + str(i), kiwi, conn)
    #     pro.start()



"""
当生产者线程的顺序在消费者线程的顺序之上/下, 同时可没有两个notifall() 方法, 
    运行过程: 先生产到最大库存量,程序陷入死循环, 可能是两个线程都挂起导致

"""