class Node:
    def __init__(self, element, pointer):
        self.element = element  # 元素值
        self.pointer = pointer  # 指向下一个元素的指针


class SinglyLinkedList:
    def __init__(self):
        self.head = None  # 指向首元结点<第一个元素>,此处没有头结点
        self.tail = None  # 指向尾节点
        self.size = 0

    def insert_head(self, data):  # 头插法
        newest = Node(data, None)
        """
        采用头插法插入新节点,需要按照如下顺序插入:
            1. 先将现在的head 赋值给新创建的节点newest的指针域
            2. 将head 赋值给新创建的newest 节点
            3. 当元素只有一个时, 尾节点即该元素,以后即使插入新元素也不会变
        """
        newest.pointer = self.head
        self.head = newest
        self.size += 1
        if self.size == 1:
            self.tail = newest

    def quick_sort(self, node):
        if not node.pointer or not node.pointer.pointer:  # 只要一个不成立就不成立,递归退层的结束标志
            return node
        origin_node = node
        pivot_node = node.pointer  # the first node
        left = Node(0, None)  # the left linked list reference
        rest_l = left
        right = Node(0, None)  # the right linked list reference
        rest_r = right
        node = node.pointer.pointer  # the second node
        while node:  # the node is not tail
            if pivot_node.element < node.element:  # move the node to the right linked list
                right.pointer = node
                right = right.pointer
            else:
                left.pointer = node  # move the node to the left linked list
                left = left.pointer
            node = node.pointer
        left.pointer = None
        right.pointer = None
        l_linked_list_reference = self.quick_sort(rest_l)  # sort the left linked list
        r_linked_list_reference = self.quick_sort(rest_r)  # sort the right linked list
        pivot_node.pointer = r_linked_list_reference.pointer  # combine pivot node and right linked list
        if not l_linked_list_reference.pointer:  # when left linked list is empty
            return origin_node  # this means the origin node is the reference I want
        else:
            now = l_linked_list_reference
            while now.pointer:
                now = now.pointer
            now.pointer = pivot_node  # traverse the whole left linked list and combine the tail's reference with pivot
            return l_linked_list_reference


# code only for check

a = SinglyLinkedList()
# a.insert_head(1)
# a.insert_head(10)
# a.insert_head(5)
# a.insert_head(2)
# a.insert_head(100)
a.insert_head(0)
node = Node('start', a.head)
new_node = a.quick_sort(node)
while new_node.pointer:  # 直接忽略头结点进行遍历
    print(new_node.pointer.element)
    new_node = new_node.pointer
