import unittest
import fque
from queue import Empty, Full


class FunctionalityTests(unittest.TestCase):
    def test_get_empty(self):
        queue = fque.Queue()
        self.assertTrue(queue.empty())
        with self.assertRaises(Empty):
            queue.get(block=False)
        with self.assertRaises(Empty):
            queue.get(timeout=0.1)

    def test_simple_get(self):
        queue = fque.Queue()
        self.assertTrue(queue.empty())
        queue.put(10)
        self.assertFalse(queue.empty())
        msg = queue.get()
        self.assertEqual(10, msg)

    def test_get_full(self):
        queue = fque.Queue(maxsize=100)
        self.assertTrue(queue.empty())
        for i in range(100):
            queue.put(1)
            self.assertFalse(queue.empty())
        self.assertTrue(queue.full())
        with self.assertRaises(Full):
            queue.put(2)

    def test_fill_and_empty(self):
        queue = fque.Queue(maxsize=100)
        self.assertTrue(queue.empty())
        for i in range(100):
            queue.put(1)
            self.assertFalse(queue.empty())
        self.assertTrue(queue.full())
        for i in range(100):
            queue.get()
            self.assertFalse(queue.full())
        self.assertTrue(queue.empty())


if __name__ == '__main__':
    unittest.main()
