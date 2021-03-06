#!python3

from prefixtreenode import PrefixTreeNode


class PrefixTree:
    """PrefixTree: A multi-way prefix tree that stores strings with efficient
    methods to insert a string into the tree, check if it contains a matching
    string, and retrieve all strings that start with a given prefix string.
    Time complexity of these methods depends only on the number of strings
    retrieved and their maximum length (size and height of subtree searched),
    but is independent of the number of strings stored in the prefix tree, as
    its height depends only on the length of the longest string stored in it.
    This makes a prefix tree effective for spell-checking and autocompletion.
    Each string is stored as a sequence of characters along a path from the
    tree's root node to a terminal node that marks the end of the string."""

    # Constant for the start character stored in the prefix tree's root node
    START_CHARACTER = ''

    def __init__(self, strings=None):
        """Initialize this prefix tree and insert the given strings, if any."""
        # Create a new root node with the start character
        self.root = PrefixTreeNode(PrefixTree.START_CHARACTER)
        # Count the number of strings inserted into the tree
        self.size = 0
        # Insert each string, if any were given
        if strings is not None:
            for string in strings:
                self.insert(string)

    def __repr__(self):
        """Return a string representation of this prefix tree."""
        return f'PrefixTree({self.strings()!r})'

    def is_empty(self):
        """Return True if this prefix tree is empty (contains no strings)."""
        # TODO
        # If the size of the string is 0, the string is empty
        return self.size == 0

    def contains(self, string):
        """Return True if this prefix tree contains the given string."""
        # TODO
        # set node as root
        node = self.root
        # loop through characters of the string
        for i in string:
            # If the current node has a child that matches
            # the current instance character
            if node.has_child(i):
                # set the node to become the character of that child
                node = node.get_child(i)

            # current node has no children matching this
            # current instance character
            else:
                # terminal == True
                return node.is_terminal()
        # if the loop ends character does not exsist
        return node.is_terminal()

    def insert(self, string):
        """Insert the given string into this prefix tree."""
        # set node as root
        node = self.root
        # TODO
        # loop through the characters of the string
        for i in string:
            # If the current node has a child that matches
            # the current instance character
            if node.has_child(i):
                # set the node to become the character of that child
                node = node.get_child(i)

            # current node has no children matching this
            # current instance character
            else:
                # Make a new node out of the current character
                new_node = PrefixTreeNode(i)
                # add this new_node as a child of this current instance
                node.add_child(i, new_node)
                # get the children of this node
                node = node.get_child(i)
        # increase size count and set terminal to True
        if not node.is_terminal():
            self.size += 1
            node.terminal = True



    def _find_node(self, string):
        """Return a pair containing the deepest node in this prefix tree that
        matches the longest prefix of the given string and the node's depth.
        The depth returned is equal to the number of prefix characters matched.
        Search is done iteratively with a loop starting from the root node."""
        # Match the empty string

        if len(string) == 0:
            return self.root, 0

        # Start with the root node
        node = self.root
        # TODO
        depth = 0
        # Loop through the characters of the string
        for i in string:
            # if the current node has children
            if node.has_child(i):
                # get the children
                node = node.get_child(i)
                # and increase the depth count
                depth += 1
            # the current node has no children
            else:
                break
        return node, depth


    def complete(self, prefix):
        """Return a list of all strings stored in this prefix tree that start
        with the given prefix string."""
        # Create a list of completions in prefix tree
        prefix_strings = []

        if prefix == '':
            return self.strings()

        # Find the deepest node of prefix
        node = self._find_node(prefix)

        # If the fist node value is not empty
        if node[0].character != '':
            # append to prefix string
            self._traverse(node[0], prefix, prefix_strings.append)

        return prefix_strings

    def strings(self):
        """Return a list of all strings stored in this prefix tree."""
        # Create a list of all strings in prefix tree
        all_strings = []

        # Traverse all nodes
        self._traverse(self.root, '', all_strings.append)

        return all_strings

    def _traverse(self, node, prefix, visit):
        """Traverse this prefix tree with recursive depth-first traversal.
        Start at the given node with the given prefix representing its path in
        this prefix tree and visit each node with the given visit function."""
        # TODO
        # if end of word, visit this node
        if node.is_terminal():
            visit(prefix)

        # traverse children recursively until end of the work, terminal == True
        for i in node.children:
            child = node.get_child(i)
            self._traverse(child, prefix + i, visit)



def create_prefix_tree(strings):
    print(f'strings: {strings}')

    tree = PrefixTree()
    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')
    print(f'strings: {tree.strings()}')

    print('\nInserting strings:')
    for string in strings:
        tree.insert(string)
        print(f'insert({string!r}), size: {tree.size}')

    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')

    print('\nSearching for strings in tree:')
    for string in sorted(set(strings)):
        result = tree.contains(string)
        print(f'contains({string!r}): {result}')

    print('\nSearching for strings not in tree:')
    prefixes = sorted(set(string[:len(string)//2] for string in strings))
    for prefix in prefixes:
        if len(prefix) == 0 or prefix in strings:
            continue
        result = tree.contains(prefix)
        print(f'contains({prefix!r}): {result}')

    print('\nCompleting prefixes in tree:')
    for prefix in prefixes:
        completions = tree.complete(prefix)
        print(f'complete({prefix!r}): {completions}')

    print('\nRetrieving all strings:')
    retrieved_strings = tree.strings()
    print(f'strings: {retrieved_strings}')
    matches = set(retrieved_strings) == set(strings)
    print(f'matches? {matches}')


def main():
    # Simpe test case of string with partial substring overlaps
    strings = ['ABC', 'ABD', 'A', 'XYZ']
    create_prefix_tree(strings)

    # Create a dictionary of tongue-twisters with similar words to test with
    tongue_twisters = {
        'Seashells': 'Shelly sells seashells by the sea shore'.split(),
        # 'Peppers': 'Peter Piper picked a peck of pickled peppers'.split(),
        # 'Woodchuck': ('How much wood would a wood chuck chuck'
        #                ' if a wood chuck could chuck wood').split()
    }
    # Create a prefix tree with the similar words in each tongue-twister
    for name, strings in tongue_twisters.items():
        print(f'{name} tongue-twister:')
        create_prefix_tree(strings)
        if len(tongue_twisters) > 1:
            print('\n' + '='*80 + '\n')


if __name__ == '__main__':
    main()
