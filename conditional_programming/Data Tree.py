class TreeNode:
    def __init__(self, char):
        self.char = char
        self.children = {}

class Tree:
    def __init__(self):
        self.root = TreeNode('')

    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TreeNode(char)
            node = node.children[char]

    def find_word(self, word):
        node = self.root
        depth = 0  # Initialize depth to 0
        for char in word:
            if char not in node.children:
                return None, -1  # Word not found, return depth -1
            node = node.children[char]
            depth += 1  # Increment depth
        return node, depth  # Return the node where the word ends and depth

# Example tree
word_tree = Tree()
words = ["apple", "banana", "cat", "dog", "elephant", "zebra"]
for word in words:
    word_tree.add_word(word)

# Query the tree
query_word = "cat"
found_node, depth = word_tree.find_word(query_word)

if found_node:
    print(f"The word '{query_word}' was found in the tree at depth {depth}.")
else:
    print(f"The word '{query_word}' was not found in the tree.")
