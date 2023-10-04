import hashlib
import unittest
from version_2 import sha_256

LENGTH = 32
EMPTY_MESSAGE = ""
SHORT_MESSAGE = "Hello, World!"
AVERAGE_MESSAGE = (
    "Special cases aren't special enough to break the rules.\n"
    "Although practicality beats purity."
    )
BYTES_MESSAGE = b"jlfdsldqfbcalmqpiorancbcamw,,;!w?ijoanwnfvbw;xww"
UNICODE_MESSAGE = (
    "Adds word-relevant emojis ❤ to text ✨ with sometimes hilarious 😂 results 😏."
    "Read more about its history 📚 and how it works"
    )
    
class TestFixedLength(unittest.TestCase):
    
    def setUp(self):
        self.test_data = open("LONG_MESSAGE.txt")
        self.LONG_MESSAGE = self.test_data.read()

    def tearDown(self):
        self.test_data.close()

    def test_empty_message(self):
        self.assertEqual(
            len(sha_256(EMPTY_MESSAGE)) , LENGTH, f"Result length should be {LENGTH}")
    
    def test_short_message(self):
        self.assertEqual(
            len(sha_256(SHORT_MESSAGE)) , LENGTH, f"Result length should be {LENGTH}")

    def test_average_message(self):
        self.assertEqual(
            len(sha_256(AVERAGE_MESSAGE)) , LENGTH, f"Result length should be {LENGTH}")

    def test_bytes_message(self):
        self.assertEqual(
            len(sha_256(BYTES_MESSAGE)) , LENGTH, f"Result length should be {LENGTH}")
    
    def test_unicode_message(self):
        self.assertEqual(
            len(sha_256(UNICODE_MESSAGE)) , LENGTH, f"Result length should be {LENGTH}")

    def test_long_message(self):
        self.assertEqual(
            len(sha_256(self.LONG_MESSAGE)) , LENGTH, 
            f"Result length should be {LENGTH}"
            )


class TestSHA256(unittest.TestCase):
    
    def setUp(self):
        self.test_data = open("LONG_MESSAGE.txt")
        self.LONG_MESSAGE = self.test_data.read()
    
    def tearDown(self):
        self.test_data.close()

    def test_empty_message(self):
        self.assertEqual(
            sha_256(EMPTY_MESSAGE), 
            hashlib.sha256(EMPTY_MESSAGE.encode("utf-8")).digest()
            )

    def test_short_message(self):
        self.assertEqual(
            sha_256(SHORT_MESSAGE), 
            hashlib.sha256(SHORT_MESSAGE.encode("utf-8")).digest()
            )

    def test_average_message(self):
        self.assertEqual(
            sha_256(AVERAGE_MESSAGE), 
            hashlib.sha256(AVERAGE_MESSAGE.encode("utf-8")).digest()
            )

    def test_bytes_message(self):
        self.assertEqual(
            sha_256(BYTES_MESSAGE), 
            hashlib.sha256(BYTES_MESSAGE).digest()
            )

    def test_unicode_message(self):
        self.assertEqual(
            sha_256(UNICODE_MESSAGE), 
            hashlib.sha256(UNICODE_MESSAGE.encode("utf-8")).digest()
            )

    def test_long_message(self):
        self.assertEqual(
            sha_256(self.LONG_MESSAGE), 
            hashlib.sha256(self.LONG_MESSAGE.encode("utf-8")).digest()
            )


if __name__ == "__main__":
    unittest.main()
    