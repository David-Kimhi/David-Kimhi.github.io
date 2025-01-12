class Line:
    """
        Represents a line, i.e. linear equation.

        :param m: the slope
        :param b: the intercept
        :param index: the index of the line in the original array (H and D)
    """

    def __init__(self, m, b, index, a_node=True):
        self.m = m
        self.b = b
        self.index = index

        # The second-best line (for left and right parts) for a node in the tree
        if a_node:
            self.second_best_right = Line(0, 0, index, not a_node)
            self.second_best_left = Line(0, 0, index, not a_node)

    def __call__(self, x):
        """
        Calculate the value of y for a given x
        :param x: x
        :return: y
        """
        return self.m * x + self.b


def insert(l, r, segment, idx=0):
    """
    Implementation of the insert function in Li-Chao tree
    :param l: left boundary
    :param r: right boundary
    :param segment: a candidate line
    :param idx: the index of the node in the tree
    :return:
    """
    # if index out of range, or if it's a 0 line (Line(0, 0))
    if (not segment.m and not segment.b) or idx >= N:
        return

    # if the range is a single value
    if l + 1 == r:
        if segment(l) > a[idx](l):
            a[idx] = segment
        return

    # calculate the middle of the range, and the indices of left and right children
    mid = (l + r) // 2
    left_son = idx * 2 + 1
    right_son = idx * 2 + 2

    # take the greater slope
    if a[idx].m > segment.m:
        a[idx], segment = segment, a[idx]

    # if the candidate is better at mid, it's better in the whole left range
    if a[idx](mid) < segment(mid):
        a[idx], segment = segment, a[idx]
        insert(l, mid, segment, left_son)

    # if it's worse at mid, it might be better in the right part
    else:
        insert(mid, r, segment, right_son)


def query(l, r, x, query_index, idx=0):
    """
    Implementation of the query function of a Li-Chao tree,
    with a small adaptation to our particular problem
    :param l: left boundary
    :param r: right boundary
    :param x: value in range
    :param query_index: the index of the initial caller to this query (i.e. the first warrior)
    :param idx: the index of the node in the tree
    :return:
    """
    if idx >= len(a):
        return 0  # return minimum score

    # Range is a single value
    if l + 1 == r:
        return a[idx](x)

    # calculate the middle of the range, and the indices of left and right children
    mid = (l + r) // 2
    left_son = idx * 2 + 1
    right_son = idx * 2 + 2

    # We're LEFT to mid
    if x < mid:

        # i != j
        if query_index != a[idx].index:
            # query the tree normally (like a normal Li-Chao tree)
            return max(a[idx](x), query(l, mid, x, query_index, left_son))

        # i = j
        else:
            # instead of the value in the current line,
            # take the maximum of the next second best lines for this node
            return max(a[idx].second_best_right(x), a[idx].second_best_left(x),
                       query(l, mid, x, query_index, left_son))

    # We're RIGHT to mid
    else:
        # i != j
        if query_index != a[idx].index:
            # query the tree normally (like a normal Li-Chao tree)
            return max(a[idx](x), query(mid, r, x, query_index, right_son))

        # i = j
        else:
            # instead of the value in the current line,
            # take the maximum of the next second best lines for this node
            return max(a[idx].second_best_right(x), a[idx].second_best_left(x),
                       query(l, mid, x, query_index, right_son))


# initiate a tree in length N
a = [Line(0, 0, i) for i in range(N)]

# Calculate the range boundaries
min_range = min(H)
max_range = max(H)

# insert all N lines sequentially
for j in range(N):
    slope_j = D[j]
    intercept_j = H[j] * D[j]
    insert(min_range, max_range, Line(slope_j, intercept_j, j))

# assign second best lines for each node of the tree
for i in range(N):
    left_son = i * 2 + 1
    right_son = i * 2 + 2
    if left_son < N:
        a[i].second_best_left = a[left_son]
    if right_son < N:
        a[i].second_best_right = a[right_son]

# query the tree for each one of the warriors, and return the maximum value
return max(D[i] * H[i] + query(min_range, max_range, H[i], i) for i in range(N)) / B