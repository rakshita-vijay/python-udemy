'''
better to test from simple (things) to complex (things)
'''
import unittest
import _009_capitalize

class TestCap(unittest.TestCase):

    def test_one_word(self):
        text = 'python'
        res = _009_capitalize.cap(text)
        self.assertEqual(res, 'Python')

    def test_many_words(self):
        text = 'monty python'
        res = _009_capitalize.cap(text)
        self.assertEqual(res, 'Monty python')

if __name__ == "__main__":
    unittest.main()


'''
unittest.main(): This is a built-in function from the unittest module.

It automatically discovers and runs all test methods that start with test in classes that inherit from unittest.TestCase.

It also provides a command-line interface to run tests, print results, and show errors/failures.

'''
