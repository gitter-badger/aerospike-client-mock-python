import unittest
import time
from AerospikeClientMock import AerospikeClientMock


class TestAerospikeClientTtlMock(unittest.TestCase):
    def setUp(self):
        pass

    def get_time(self, ttl=0):
        return int(time.time()) + ttl

    def test_blank_init(self):
        asm = AerospikeClientMock(default_ttl=2)
        self.assertEqual("{}", str(asm))

    def test_connected(self):
        asm = AerospikeClientMock(default_ttl=2)
        self.assertTrue(asm.is_connected())

    def test_put(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEqual("{('a', 'b', 'c'): {'a': 1}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))
        time.sleep(1)
        asm.put(key, {"a": 1})
        self.assertEqual("(('a', 'b', 'c'), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))
        asm.put(key, {"a": 1}, meta={"ttl": 1})
        self.assertEqual("(('a', 'b', 'c'), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(1)) + "})", str(asm.get(key)))

    def test_incr(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        asm.increment(key, "a", 2)
        self.assertEqual("{('a', 'b', 'c'): {'a': 3}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'a': 3}, {'gen': 2, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))
        asm.increment(key, "a", 1, meta={"ttl": 1})
        self.assertEqual("(('a', 'b', 'c'), {'a': 4}, {'gen': 3, 'ttl': " + str(self.get_time(1)) + "})", str(asm.get(key)))

    def test_undefined_incr(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.increment(key, "a", 1)
        self.assertEqual("{('a', 'b', 'c'): {'a': 1}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))

    def test_append(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.put(key, {"word": "ello"})
        asm.prepend(key, "word", "h")
        self.assertEqual("{('a', 'b', 'c'): {'word': 'hello'}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'word': 'hello'}, {'gen': 2, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))

    def test_prepend(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.put(key, {"word": "hell"})
        asm.append(key, "word", "o")
        self.assertEqual("{('a', 'b', 'c'): {'word': 'hello'}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'word': 'hello'}, {'gen': 2, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))

    def test_get(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl = 2)
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEqual("(('a', 'b', 'c'), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))
        # test if not changing gen
        self.assertEqual("(('a', 'b', 'c'), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))

    def test_exists(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEquals((True, {'gen': 1, 'ttl': self.get_time(default_ttl)}), asm.exists(key))
        # test if not changing gen
        self.assertEquals((True, {'gen': 1, 'ttl': self.get_time(default_ttl)}), asm.exists(key))

    def test_expire_exist(self):
        asm = AerospikeClientMock(default_ttl=1)
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        time.sleep(2)
        self.assertEquals((False, None), asm.exists(key))

    def test_not_exists(self):
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        self.assertEquals((False, None), asm.exists(key))

    def test_touch(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.put(key, {"a": 1})
        self.assertEquals("(('a', 'b', 'c'), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))
        time.sleep(1)
        asm.touch(key)
        self.assertEquals("(('a', 'b', 'c'), {'a': 1}, {'gen': 2, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))
        asm.touch(key, 4)
        self.assertEquals("(('a', 'b', 'c'), {'a': 1}, {'gen': 3, 'ttl': " + str(self.get_time(4)) + "})", str(asm.get(key)))

    def test_remove_bin(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        key = ("a", "b", "c")
        asm.put(key, {"a": 1, "b": 1, "c": 1, "d": 1})
        self.assertEquals("{('a', 'b', 'c'): {'a': 1, 'c': 1, 'b': 1, 'd': 1}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'a': 1, 'c': 1, 'b': 1, 'd': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))
        asm.remove_bin(key, ["b", "d"], meta={"ttl": 4})
        self.assertEquals("{('a', 'b', 'c'): {'a': 1, 'c': 1}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'a': 1, 'c': 1}, {'gen': 2, 'ttl': " + str(self.get_time(4)) + "})", str(asm.get(key)))
        asm.remove_bin(key, ["c"])
        self.assertEquals("{('a', 'b', 'c'): {'a': 1}}", str(asm))
        self.assertEqual("(('a', 'b', 'c'), {'a': 1}, {'gen': 3, 'ttl': " + str(self.get_time(default_ttl)) + "})", str(asm.get(key)))

    def test_get_many(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        asm.put(("a", "b", 1), {"a": 1})
        asm.put(("a", "b", 2), {"a": 2})
        asm.put(("a", "b", 3), {"a": 3})
        asm.put(("a", "b", 4), {"a": 4})
        keys = [
            ("a", "b", 1),
            ("a", "b", 2),
            ("a", "b", 3),
            ("a", "b", 4),
            ("a", "b", 5),
        ]
        self.assertEqual("{1: (('a', 'b', 1), {'a': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 2: (('a', 'b', 2), {'a': 2}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 3: (('a', 'b', 3), {'a': 3}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 4: (('a', 'b', 4), {'a': 4}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 5: None}", str(asm.get_many(keys)))

    def test_exists_many(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        asm.put(("a", "b", 1), {"a": 1})
        asm.put(("a", "b", 2), {"a": 2})
        asm.put(("a", "b", 3), {"a": 3})
        asm.put(("a", "b", 4), {"a": 4})
        keys = [
            ("a", "b", 1),
            ("a", "b", 2),
            ("a", "b", 3),
            ("a", "b", 4),
            ("a", "b", 5),
        ]
        self.assertEqual("{1: {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}, 2: {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}, 3: {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}, 4: {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}, 5: None}", str(asm.exists_many(keys)))

    def test_select_many(self):
        default_ttl = 2
        asm = AerospikeClientMock(default_ttl=2)
        asm.put(("a", "b", 1), {"a": 1, "b": 1})
        asm.put(("a", "b", 2), {"a": 2, "b": 2})
        asm.put(("a", "b", 3), {"a": 3, "b": 3})
        asm.put(("a", "b", 4), {"a": 4, "b": 4})
        keys = [
            ("a", "b", 1),
            ("a", "b", 2),
            ("a", "b", 3),
            ("a", "b", 4),
            ("a", "b", 5),
        ]
        self.assertEqual("{('a', 'b', 3): {'a': 3, 'b': 3}, ('a', 'b', 2): {'a': 2, 'b': 2}, ('a', 'b', 4): {'a': 4, 'b': 4}, ('a', 'b', 1): {'a': 1, 'b': 1}}", str(asm))
        self.assertEqual("{1: (('a', 'b', 1), {'a': 1, 'b': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 2: (('a', 'b', 2), {'a': 2, 'b': 2}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 3: (('a', 'b', 3), {'a': 3, 'b': 3}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 4: (('a', 'b', 4), {'a': 4, 'b': 4}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 5: None}", str(asm.select_many(keys, ["a", "b"])))
        self.assertEqual("{1: (('a', 'b', 1), {'b': 1}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 2: (('a', 'b', 2), {'b': 2}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 3: (('a', 'b', 3), {'b': 3}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 4: (('a', 'b', 4), {'b': 4}, {'gen': 1, 'ttl': " + str(self.get_time(default_ttl)) + "}), 5: None}", str(asm.select_many(keys, ["b"])))


if __name__ == '__main__':
    unittest.main()