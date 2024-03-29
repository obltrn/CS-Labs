# Lab 4 - Option B
# Zybooks and Dr. Fuentes' BTree implememtation were used for references to assist with BTree

# Tree node class
class TreeNode(object):
    left = None
    right = None
    height = 1

    def __init__(self, val):
        self.val = val

# AVL Tree clss
class AVL_Tree(object):

    #insert function
    def insert(self, root, key):

        # 1) Perform BT
        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2) Update height of ancestor node
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        #3) Get balance factor: used to get the difference between the left and the right side of the tree
        balance = self.get_balance(root)

        # 4) If unbalanced node, perform 1 of 4 possible rotations
        # Rotation 1 - Left Left
        if balance > 1 and key < root.left.val:
            return self.right_rotate(root)

        # Rotation 2 - Right Right
        if balance < -1 and key > root.right.val:
            return self.left_rotate(root)

        # Rotation 3 - Left Right
        if balance > 1 and key > root.left.val:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Rotation 4 - Right Left
        if balance < -1 and key < root.right.val:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Performs left rotation
    def left_rotate(self, root):

        temp = root.right
        sub_tree = temp.left

        # Perform rotation
        temp.left = root
        root.right = sub_tree

        # Update heights
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        temp.height = 1 + max(self.get_height(temp.left),
                              self.get_height(temp.right))

        return temp

    # Performs right rotation
    def right_rotate(self, root):

        temp = root.left
        sub_tree = temp.right

        # Perform rotation
        temp.right = root
        root.left = sub_tree

        # Update heights
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        temp.height = 1 + max(self.get_height(temp.left),
                              self.get_height(temp.right))

        return temp

    # Gets the height of the node
    def get_height(self, root):
        if not root:
            return 0

        return root.height

    # Gets the balance factor between left and right side
    def get_balance(self, root):
        if not root:
            return 0

        return self.get_height(root.left) - self.get_height(root.right)

#Searching for word in txt file
def find_word(root, word):
    if root is None:
        return False

    if root.val.lower() == word.lower():  # every search is done in lower case.
        return True

    # Pre order search.
    if find_word(root.left, word) or find_word(root.right, word):
        return True

    return False


def max_anagrams(text_file, root):
    # open file and clean the input.
    file_reader = open(text_file, "r")
    word_list = [line.rstrip() for line in file_reader.readlines()]

    # tracking the word with most anagrams
    most_anagrams = ""
    max_num = -1

    for word in word_list:
        # print(word)  # testing
        anagram_count = count_anagrams(root, word)
        if anagram_count > max_num:
            most_anagrams = word
            max_num = anagram_count

    return most_anagrams


class BTreeNode:
    # Constructor
    def __init__(self, keys=[], children=[], is_leaf=True, max_num_keys=5):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf
        if max_num_keys < 3:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys = 3
        if max_num_keys % 2 == 0:  # max_num_keys must be odd and greater or equal to 3
            max_num_keys += 1
        self.max_num_keys = max_num_keys

    def is_full(self):
        return len(self.keys) >= self.max_num_keys


class BTree:
    # Constructor
    def __init__(self, max_num_keys=5):
        self.max_num_keys = max_num_keys
        self.root = BTreeNode(max_num_keys=max_num_keys)

    def find_child(self, k, node=None):
        # Determines value of c, such that k must be in subtree node.children[c], if k is in the BTree
        if node is None:
            node = self.root

        for i in range(len(node.keys)):
            if k < node.keys[i]:
                return i
        return len(node.keys)

    def search(self, k, node=None):
        k = k.lower()  # only for strings
        if node is None:
            node = self.root
        # Returns node where k is, or None if k is not in the tree
        if k in node.keys:
            return True
        if node.is_leaf:
            return False
        return self.search(k, node.children[self.find_child(k, node)])

    def split(self, node=None):
        if node is None:
            node = self.root
        # print('Splitting')
        # PrintNode(T)
        mid = node.max_num_keys // 2
        if node.is_leaf:
            left_child = BTreeNode(node.keys[:mid], max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], max_num_keys=node.max_num_keys)
        else:
            left_child = BTreeNode(node.keys[:mid], node.children[:mid + 1], node.is_leaf, max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], node.children[mid + 1:], node.is_leaf, max_num_keys=node.max_num_keys)
        return node.keys[mid], left_child, right_child

    def insert_leaf(self, i, node=None):
        if node is None:
            node = self.root

        node.keys.append(i)
        node.keys.sort()

    def leaves(self, node=None):
        if node is None:
            node = self.root
        # Returns the leaves in a b-tree
        if node.is_leaf:
            return [node.keys]
        s = []
        for c in node.children:
            s = s + self.leaves(c)
        return s

    def insert(self, i, node=None):
        i = i.lower()  # Making words lowercase to all variations
        if node is None:
            node = self.root
        if not node.is_full():
            self.insert_internal(i, node)
        else:
            m, l, r = self.split(node)
            node.keys = [m]
            node.children = [l, r]
            node.is_leaf = False
            k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def insert_internal(self, i, node=None):

        if node is None:
            node = self.root

        # node cannot be Full
        if node.is_leaf:
            self.insert_leaf(i, node)
        else:
            k = self.find_child(i, node)
            if node.children[k].is_full():
                m, l, r = self.split(node.children[k])
                node.keys.insert(k, m)
                node.children[k] = l
                node.children.insert(k + 1, r)
                k = self.find_child(i, node)
            self.insert_internal(i, node.children[k])

    def height(self, node=None):
        if node is None:
            node = self.root
        if node.is_leaf:
            return 0
        return 1 + self.height(node.children[0])

#prints out all the words that are an anagram
def print_anagrams(tree, word, prefix=""):
    if len(word) <= 1:
        string = prefix + word
        #  print("String: %s\tPrefix: %s\tWord: %s" % (string, prefix, word))

        #  if find_word(root, string):  # searching the data structure
        if tree.search(string):
            print(string)

    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]  # letters before cur
            after = word[i + 1:]  # letters after cur

            if cur not in before:  # Check if permutations of cur have not been generated.
                print_anagrams(tree, before + after, prefix + cur)


#Returns the total number of anagrams per word
def count_anagrams(tree, word, prefix=""):
    total = 0
    if len(word) <= 1:
        string = prefix + word
        # print("String: %s\tPrefix: %s\tWord: %s" % (string, prefix, word))

        if tree.search(string):
            return 1 

    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]  # letters before cur
            after = word[i + 1:]  # letters after cur

            # Check if permutations of cur have not been generated.
            if cur not in before:  
                total += count_anagrams(tree, before + after, prefix + cur) 

    return total


def max_anagrams(text_file, tree):
    # open file and clean the input.
    file_reader = open(text_file, "r")
    word_list = [line.rstrip() for line in file_reader.readlines()]

    # tracking the word with most anagrams
    most_anagrams = ""
    max_num = -1

    for word in word_list:
        # print(word)  # testing
        anagram_count = count_anagrams(tree, word)
        if anagram_count > max_num:
            most_anagrams = word
            max_num = anagram_count

    return most_anagrams



def main():
    # read the files
    raw_words = open("words.txt", "r")

    # set the content of the files into lists & combine them
    words = [line.rstrip() for line in raw_words.readlines()]

    tree = BTree(max_num_keys=5)

    for w in words:
        tree.insert(w)

    print(tree.search("Aalst"))

    print_anagrams(tree, "stop")

    total_anagrams = count_anagrams(tree, "stop")

    print("Stop has %d anagrams" % total_anagrams)

    test_file = "anagrams.txt"
    max_anagram = max_anagrams(test_file, tree)

    print("The word with most anagrams is: " + max_anagram)

    # print_anagrams(tree, max_anagram)


