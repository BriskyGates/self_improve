**Prerequisite**
- collection.py 利用两个线程分别消费和生产goods
- goods.py 用来控制goods 的生产和消费
- producer.py用来控制goods的生产线程
- consumer.py 用来控制goods的消费线程

**Codes for theading**
- 因为继承 Thead父类,需要传入线程名给父类
- 复写run()方法
- run()大致的框架是: 
 - - 第一层while True循环,
 - - 第二层主要是获取线程锁对象,防止共享资源无法正确读写
- - - 判断当前goods的数量来决定是否要生产还是消费,如果是前者,调用goods 相关的生产代码,
        否则 则需要通知线程中在等待吗的消费线程, 利用wait() 释放锁
- - - 每生产完一个goods后都会释放锁