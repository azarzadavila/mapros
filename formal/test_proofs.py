from django.test import TestCase

from formal.proof import check_scope


class SimpleUnits(TestCase):
    def test_scope(self):
        self.assertTrue(check_scope((1,), (2,)))
        self.assertTrue(check_scope((1,), (2, 1)))
        self.assertTrue(check_scope((1,), (2, 1, 3)))
        self.assertTrue(check_scope((2, 1), (2, 3)))
        self.assertTrue(check_scope((2, 1), (2, 3, 2)))
        self.assertFalse(check_scope((3,), (2,)))
        self.assertFalse(check_scope((1, 1), (2,)))
        self.assertFalse(check_scope((2, 1, 1), (2, 2,)))
        self.assertTrue(check_scope((2, 1, 1), (2, 1,)))
