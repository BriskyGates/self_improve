#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
"""


class TreeSet:
    def __init__(self):
        self.__set = set()

    def values(self):
        return sorted(self.__set)

    def add(self, val):
        self.__set.add(val)

    def remove(self, val):
        if val in self.__set:
            self.__set.remove(val)

    def higher(self, val):
        """
        找到比val 更大的下一个值
        Args:
            val:

        Returns:

        """
        if self.the_max() < val:
            return None
        if self.the_min() > val:
            return self.the_min()
        vals = self.values()  # 已经排好序的列表
        low = 0
        up = self.size() - 1  # 最大值
        while low <= up:  # 二分查找,前提条件就是列表有序
            mid = (low + up) // 2
            if vals[mid] <= val:
                low = mid + 1
            elif vals[mid - 1] <= val:  # 如果中间-1 位置上面的数<=val, 那么中间位置即是要找的值
                return vals[mid]
            else:  # vals[mid]>val,则需要调整up的值
                up = mid - 1

    def the_max(self):
        if not self.__set:
            return -1
        return max(self.__set)

    def the_min(self):
        if not self.__set:
            return -1
        return min(self.__set)

    def size(self):
        return len(self.__set)

    def is_empty(self):
        return self.size() == 0
