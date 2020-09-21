import unittest
from typing import Any

from ojos.exception import BaseException
from ojos.sys import lazy_loader


class TestBaseException(unittest.TestCase):
    def setUp(self):
        self.excption = BaseException("name", "value")

    def tearDown(self):
        pass

    def test_ok(self):
        self.assertEqual(self.excption.message, "Exception name: value")


class TestLazyLoader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_single_depth(self):
        uuid: Any = lazy_loader("uuid")
        self.assertTrue(isinstance(uuid.uuid4(), uuid.UUID))

    def test_multiple_depth(self):
        datetime: datetime = lazy_loader("datetime.datetime")
        self.assertTrue(isinstance(datetime.now(), datetime))


if __name__ == "__main__":
    unittest.main()
