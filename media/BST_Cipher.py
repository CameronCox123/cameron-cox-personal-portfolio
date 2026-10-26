#  File: BST_Cipher.py
#  Student Name: Cameron Cox
#  Student UT EID: cpc2526
#  Partner Name: Julian Pineros
#  Partner UT EID: jp65362

#  Program Description: Creates an Cipher using a binary search tree and a given message 'key'
#  The encryption uses the binary tree, a root node is created from the first letter in our message
#  Letters are added to our tree based on the order of the message.
#  When encrypting letters will be translated to symbols. A '<' means we went left once in the
#  Binary tree, a '>' means we went right, a '*' means it was the root, and a '!' stands for a space

import sys


# One node in the BST Cipher Tree
class Node:
    def __init__(self, ch):
        self.ch = ch
        self.left = None
        self.right = None


# The BST Cipher Tree
class Tree:

    # Create the BST Cipher tree based on the key
    def __init__(self, key):
        # Make sure we have an appropriate key
        self.root = None
        key = self.clean(key)
        cleanString = ""
        key = key.lower()
        for character in key:
            if character not in cleanString:
                cleanString += character

        # Create the tree after we've finalized our string 
        for i in cleanString:
            self.insert(i)

    # Inserts one new charater/Node to the BST Cipher tree
    # If the character already exists, don't add it.
    def insert(self, ch):
        self.root = self.insert_helper(self.root, ch)

    # Use recursion to insert a specific letter in the tree based on our key
    def insert_helper(self, current, ch):
        if current is None:
            return Node(ch)

        if ch < current.ch:
            current.left = self.insert_helper(current.left, ch)
        else:
            current.right = self.insert_helper(current.right, ch)

        return current

    # Encrypts a text message using the BST Tree
    def encrypt(self, message):
        message = self.clean(message)
        encrypted_message = ''
        # Adds encrypted message for each character in the message
        for char in message:
            encrypted_message += self.encrypt_ch(char)
        encrypted_message = encrypted_message[:-1]
        return encrypted_message

    # Encrypts a single character
    def encrypt_ch(self, ch):
        encrypted_message = ''
        current = self.root
        # While the current node is not none, adds symbol to encrypted message dependent on node
        while current is not None:
            # Checks if node data equals ch and adds appropriate symbol
            if current.ch == ch and current == self.root:
                encrypted_message += '*!'
                current = None
            elif current.ch == ch:
                encrypted_message += '!'
                current = None
            elif ch < current.ch:
                current = current.left
                encrypted_message += '<'
            else:
                current = current.right
                encrypted_message += '>'
        return encrypted_message

    # Decrypts an encrypted message using the BST Tree
    def decrypt(self, codes_string):
        decrypted_message = ''
        # Splits the codes for each character and puts them in list
        listOfCodes = codes_string.split("!")
        # For each code in the list of codes, decrypts code and adds to decrypted message
        for code in listOfCodes:
            decrypted_message += self.decrypt_code(code)
        return decrypted_message

    # Decrypts a single code
    def decrypt_code(self, code):
        decrypted_message = ''
        current = self.root
        # Checks to see if code is correct
        isValidCode = True
        # For each char in code, adds decrypted char to decrypted message
        for char in code:
            # Checks symbol, and makes appropriate movement
            if char == '<':
                if current.left is not None:
                    current = current.left
                    isValidCode = True
                else:
                    isValidCode = False
            elif char == '>':
                if current.right is not None:
                    current = current.right
                    isValidCode = True
                else:
                    isValidCode = False
        # Adds decrypted character if the code was valid
        if isValidCode:
            decrypted_message += current.ch
        return decrypted_message

    # Get printed version of BST for debugging
    def BST_print(self):
        if self.root is None:
            return "Empty tree"
        self.BST_print_helper(self.root)

    # Prints a BST subtree
    def BST_print_helper(self, node, level=0):
        if node is not None:
            if node.right is not None:
                self.BST_print_helper(node.right, level + 1)
            print('     ' * level + '->', node.ch)
            if node.left is not None:
                self.BST_print_helper(node.left, level + 1)

    # Utility method
    def clean(self, text):
        cleanText = ""
        for i in range(len(text)):
            if (self.isValidCh(text[i])):
                cleanText += text[i]
        return cleanText

    # Utility method
    def isValidLetter(self, ch):
        if (ch >= "a" and ch <= "z"):
            return True
        return False

    # Utility method
    def isValidCh(self, ch):
        if (ch == " " or self.isValidLetter(ch)):
            return True
        return False


''' ##### DRIVER CODE #####
    ##### Do not change, except for the debug flag '''


def main():
    # Debug flag - set to False before submitting
    debug = False
    if debug:
        in_data = open('bst_cipher.in')
    else:
        in_data = sys.stdin

    # read encryption key
    key = in_data.readline().strip()

    # create a Tree object
    key_tree = Tree(key)

    # read string to be encrypted
    text_message = in_data.readline().strip()

    # print the encryption
    print(key_tree.encrypt(text_message))

    # read the string to be decrypted
    coded_message = in_data.readline().strip()

    # print the decryption
    print(key_tree.decrypt(coded_message))


if __name__ == "__main__":
    main()