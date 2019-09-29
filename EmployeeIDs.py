import os, sys, time

from node import Node


def swap_nodes(node_a, node_b):
    temp = node_a.item
    node_a.item = node_b.item
    node_b.item = temp


def linkedlist_bubble_sort(head_node):

    sorted_node = None
    done = False

    while not done:  # if no more sorting is taking place then we stop
        done = True
        i_node = head_node  # grab the first element to start comparing

        while i_node.next is not sorted_node:    # iterate through the unsorted nodes
            if i_node.item > i_node.next.item:   # if the next node is larger we swap
                swap_nodes(i_node, i_node.next)
                done = False
                # There was a swap so we need to start checking from the head
                # at least one more time

            i_node = i_node.next

        sorted_node = i_node  # largest element, no need to go past it

    return head_node


# finds middle node of list in order to divide the list
def get_middle_node(head):

    if head is None:
        return head

    middle = head
    skip = head

    # skip pointer is used to get to the end of the list (skips one node)
    # middle pointer will be at the middle when skip reaches none
    while skip.next and skip.next.next:
        middle = middle.next
        skip = skip.next.next

    # we need to separate the lists
    next_of_middle = middle.next
    middle.next = None

    return next_of_middle


def sort_list(node_a, node_b):

    if node_a is None:
        return node_b

    if node_b is None:
        return node_a

    merged_list = None

    # rearranges nodes based off of which one is smaller (in order to sort)
    if node_a.item <= node_b.item:
        merged_list = node_a
        merged_list.next = sort_list(node_a.next, node_b)
    else:
        merged_list = node_b
        merged_list.next = sort_list(node_a, node_b.next)

    return merged_list


def linked_list_merge_sort(head_node):

    # base case
    if head_node is None or head_node.next is None:
        return head_node

    middle = get_middle_node(head_node)

    left_linked_list = linked_list_merge_sort(head_node)
    right_linked_list = linked_list_merge_sort(middle)

    sorted_list = sort_list(left_linked_list, right_linked_list)

    return sorted_list


def initialize_liked_list(arr):

    head_node = Node(-1, None)
    iteration_node = head_node

    for values in arr:
        iteration_node.next = Node(values, None)
        iteration_node = iteration_node.next

    return head_node.next


def main():
    node = Node(4, None)
    dir = os.listdir(os.getcwd())
    # print(dir)
    # print(node.item)

    # read the files
    activision = open("activision.txt", "r")
    vivendi = open("vivendi.txt", "r")

    # set the content of the files into lists & combine them
    act_list = [int(line.rstrip()) for line in activision.readlines()]
    viv_list = [int(line.rstrip()) for line in vivendi.readlines()]

    employee_list = act_list + viv_list

    # make the list into a linked list
    head_node = initialize_liked_list(employee_list)

    # Solution 1
    i_node = head_node
    r_list = []
    start_timer = time.time()

    while i_node.next:
        j_node = i_node.next  # grab the node i th node
        while j_node:         # and compare to the rest of the linked list
            if j_node.item == i_node.item:
                r_list.append(i_node.item)  # if it exists we append to a list

            j_node = j_node.next
        i_node = i_node.next
    end_timer = time.time()
    print("Solution 1 runtime = %f" % (end_timer - start_timer))

    print("Size of list is: %d" % len(r_list))

    # Solution 2
    head_node = linkedlist_bubble_sort(head_node)  # using head_node from solution 1
    i_node = head_node
    r2_list = []
    start_timer2 = time.time()

    while i_node.next:
        if i_node.item == i_node.next.item:  # compare node to partner
            r2_list.append(i_node.item)      # if it exists append to list
            i_node = i_node.next             # and skip a node

        i_node = i_node.next

    end_timer2 = time.time()
    print("Solution 2 runtime = %f" % (end_timer2 - start_timer2))
    print("Size of list 2 is: %d" % len(r2_list))

    # Solution 3
    # Python only allows 2,000 recursions. We need more for this solution
    sys.setrecursionlimit(10000)

    head_node = initialize_liked_list(employee_list)

    head_node = linked_list_merge_sort(head_node)

    # Using solution 2 code to compare neighbors
    i_node = head_node
    r3_list = []
    start_timer3 = time.time()

    while i_node.next:
        if i_node.item == i_node.next.item:
            r3_list.append(i_node.item)
            i_node = i_node.next

        i_node = i_node.next

    end_timer3 = time.time()
    print("Solution 3 runtime = %f" % (end_timer3 - start_timer3))
    print("Size of list 3 is: %d" % len(r3_list))

    # i_node = head_node

    # while i_node:
    #     print("value: %d" % i_node.item)
    #     i_node = i_node.next

    # solution 4
    m = 6000 + 1  # Activision ID's has the most

    # Initiating boolean array
    seen = []
    start_timer4 = time.time()
    for x in range(m):
        seen.append(False)

    head_node = initialize_liked_list(employee_list)

    i_node = head_node
    r4_list = []

    while i_node:
        if not seen[i_node.item]:           # if the item has not been seen mark true
            seen[i_node.item] = True
        else:                               # since it has been seen we append to repeat list
            r4_list.append(i_node.item)
        i_node = i_node.next

    end_timer4 = time.time()
    print("Solution 4 runtime = %f" % (end_timer4 - start_timer4))
    print("Size of list 4 is: %d" % len(r4_list))


main()
