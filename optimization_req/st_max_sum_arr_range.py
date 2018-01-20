# Solution to problem 'GSS1 - Can you answer these queries I' on SPOJ (but reauire optimization)


from math import log2
import sys

class Node(object):
    """
     Structure of node of the segment tree
     : tot_sum - Contains the total sum of all the the elements
                 in a specific range
     : prefix_sum - contains
    """
    def __init__(self):
        self.tot_sum = None
        self.prefix_sum = None
        self.suffix_sum = None
        self.max_sum = None

class SegmentTree(object):
    def __init__(self, n):
        self.Tree = [None] * (2*2**(int(log2(n)) + 1))

    def merge(self,result, left, right):
        result.tot_sum =  left.tot_sum + right.tot_sum
        result.prefix_sum = max(left.prefix_sum, left.tot_sum + right.prefix_sum)
        result.suffix_sum = max(right.suffix_sum,  right.tot_sum + left.suffix_sum)
        result.max_sum = max(left.max_sum, right.max_sum, left.suffix_sum + right.prefix_sum)
 
    def build(self, start, end, node, arr):
        if end < start:
            return
        if start == end:
            self.Tree[node] = Node()
            self.Tree[node].tot_sum = arr[start]
            self.Tree[node].prefix_sum = arr[start]
            self.Tree[node].suffix_sum = arr[start]
            self.Tree[node].max_sum = arr[start]
        else:
            mid = (start + end)// 2
            self.build(start, mid, 2*node + 1, arr)
            self.build(mid + 1, end, 2*node + 2, arr)
            self.Tree[node] = Node()
            self.merge(self.Tree[node], self.Tree[node*2 + 1], self.Tree[node*2 + 2])

    def query(self, start, end,  left, right, node):
        # optimization required( to be done)
        result = Node()
        result.tot_sum = result_prefix_sum = -sys.maxsize
        result.suffix_sum = result.max_sum = -sys.maxsize 
        if start >= left and  end <= right:
            return self.Tree[node]
        if end < left or right < start:
            return None
        mid = (start + end) // 2
        temp1 = temp2 = None
        if left > mid:
            return self.query(mid + 1, end, left, right, 2*node + 2)
        if right <= mid:
            return self.query(start, mid, left, right, 2*node + 1)
        temp1 = self.query(start, mid, left, right, 2*node + 1)
        temp2 = self.query(mid + 1, end, left, right, 2*node + 2)
        self.merge(result, temp1, temp2)
        return result

N = eval(input())
arr = list(map(int, input().split()))
segTree = SegmentTree(N)
segTree.build(0, N - 1, 0, arr)
q = eval(input())
for i in range(q):
    x, y = list(map(int, input().split()))
    print(segTree.query(0, N - 1, x, y, 0).max_sum)

