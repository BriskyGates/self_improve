class Node:
    def __init__(self, element, pointer):
        self.element = element
        self.pointer = pointer


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_head(self, data):  # head insert algorithm
        newest = Node(data, None)
        newest.pointer = self.head
        self.head = newest
        self.size += 1
        if self.size == 1:
            self.tail = newest

    def quick_sort(self, node):
        if not node.pointer or not node.pointer.pointer:  # to keep there is always 2 elements, but why
            return node
        origin_node = node
        pivot_node = node.pointer  # the real first node
        left = Node(0, None)  # the left linked list reference
        rest_l = left
        right = Node(0, None)  # the right linked list reference
        rest_r = right
        node = node.pointer.pointer  # the real second node
        while node:  # the node is not tail
            if pivot_node.element < node.element:  # move the node to the right linked list
                right.pointer = node
                right = right.pointer  # move the right pointer to next element
                # right = node  # move the right pointer to next element
            else:
                left.pointer = node  # move the node to the left linked list
                left = left.pointer

            node = node.pointer

        left.pointer = None  # devide all the left linked list and let the final element to None
        right.pointer = None
        l_linked_list_reference = self.quick_sort(rest_l)  # sort the left linked list
        r_linked_list_reference = self.quick_sort(rest_r)  # sort the right linked list
        pivot_node.pointer = r_linked_list_reference.pointer  # combine pivot node and right linked list
        if not l_linked_list_reference.pointer:  # when left linked list is empty
            return origin_node  # this means the origin node is the reference I want
        else:
            now = l_linked_list_reference
            while now.pointer:
                now = now.pointer  # when l_linked_list_reference is sorted, travel to the last element of left and connected it to the pivot node
            now.pointer = pivot_node  # traverse the whole left linked list and combine the tail's reference with pivot
            return l_linked_list_reference


# code only for check

a = SinglyLinkedList()
a.insert_head(1)
a.insert_head(10)
a.insert_head(-10)
a.insert_head(2)
# a.insert_head(5)
# a.insert_head(2)
# a.insert_head(100)
# a.insert_head(0)
node = Node('start', a.head)
new_node = a.quick_sort(node)  # the new_node is with "node start"

while new_node.pointer:
    print(new_node.pointer.element)
    new_node = new_node.pointer
