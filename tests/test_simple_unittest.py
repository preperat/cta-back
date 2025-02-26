import unittest

class TestSimple(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)
        print("Test ran successfully!")

if __name__ == "__main__":
    unittest.main() 