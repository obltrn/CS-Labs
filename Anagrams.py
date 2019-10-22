class TreeNode(object):
    left = None
    right = None
    height = 1

    def __init__(self, val):
        self.val = val

class AVL_Tree(object):

    def insert(self, root, key):


        if not root:
            return TreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))
        balance = self.get_balance(root)
        
        # Left Left
        if balance > 1 and key < root.left.val:
            return self.right_rotate(root)

        # Right Right
        if balance < -1 and key > root.right.val:
            return self.left_rotate(root)

        # Left Right
        if balance > 1 and key > root.left.val:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left
        if balance < -1 and key < root.right.val:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

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

    def get_height(self, root):
        if not root:
            return 0

        return root.height

    def get_balance(self, root):
        if not root:
            return 0

        return self.get_height(root.left) - self.get_height(root.right)


def find_word(root, word):
    if root is None:  
        return False
    
    # Search done in lower case
    if root.val.lower() == word.lower():
        return True

    # Pre order search.
    if find_word(root.left, word) or find_word(root.right, word):
        return True

    return False


def print_anagrams(root, word, prefix=""):
    if len(word) <= 1:
        string = prefix + word

        # searching the data structure
        if find_word(root, string):  
            print(string)

    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]  # letters before cur
            after = word[i + 1:]  # letters after cur
            
            # Check permutations
            if cur not in before:  
                print_anagrams(root, before + after, prefix + cur)

def count_anagrams(root, word, prefix=""):
    total = 0
    if len(word) <= 1:
        string = prefix + word


        if find_word(root, string):
            return 1  

    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i]  # letters before cur
            after = word[i + 1:]  # letters after cur

            #Check Permutations
            if cur not in before:  
                total += count_anagrams(root, before + after, prefix + cur) 

    return total


def max_anagrams(text_file, root):
    # open file and clean the input.
    file_reader = open(text_file, "r")
    word_list = [line.rstrip() for line in file_reader.readlines()]

    # tracking the word
    most_anagrams = ""
    max_num = -1

    for word in word_list:
        anagram_count = count_anagrams(root, word)
        if anagram_count > max_num:
            most_anagrams = word
            max_num = anagram_count

    return most_anagrams


def main():
    # read the files
    raw_words = open("words.txt", "r")

    # set the content of the files into lists & combine them
    words = [line.rstrip() for line in raw_words.readlines()]

    tree = AVL_Tree()
    r = None

    for w in words:
        r = tree.insert(r, w)

    test_word = "Abrus"
    result = find_word(r, test_word)

    print("Word: %s found: %r" % (test_word, result))

    print_anagrams(r, "stop")

    total_anagrams = count_anagrams(r, "stop")

    print("Stop has %d anagrams" % total_anagrams)

    test_file = "anagrams.txt"
    max_anagram = max_anagrams(test_file, r)

    print("The word with most anagrams is: " + max_anagram)


main()
