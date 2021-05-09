class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        n1 = len(word1)
        n2 = len(word2)
        dp = [[0] * (n2 + 1) for _ in range(n1 + 1)]
        # 第一行
        for j in range(1, n2 + 1):
            dp[0][j] = dp[0][j - 1] + 1
        # 第一列
        for i in range(1, n1 + 1):
            dp[i][0] = dp[i - 1][0] + 1

        for i in range(1, n1 + 1):
            for j in range(1, n2 + 1):
                if word1[i - 1] == word2[j - 1]:  # 对word1 word2而言还是需要从0开始
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]) + 1
        print(dp[-1][-1])
        return dp[-1][-1]


def levenshtein(first, second):
    if len(first) > len(second):  # 保证长度小的在后
        first, second = second, first

    if len(first) == 0:  # 空字符替换成second
        return len(second)
    if len(second) == 0:  # xxx 替换成空
        return len(first)

    first_length = len(first) + 1
    second_length = len(second) + 1
    """因为在此初始化每行都是从0~ second_length, 需要借用上面根据长度返回相应的数值"""
    distance_matrix = [list(range(second_length)) for x in range(first_length)]
    # print distance_matrix

    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)

    print(distance_matrix[-1][-1])
    return distance_matrix[-1][-1]


if __name__ == '__main__':
    Solution().minDistance('aba', '')
    levenshtein('aba', '')
"""形式5*8的矩阵"""
