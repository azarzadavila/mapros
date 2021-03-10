from typing import Type

from main.context import Context
from main.language import Language


def test_bijective(self, cls: Type[Language], natural, lean, context=None):
    if context is None:
        context = Context()
    obj = cls.from_natural(natural, context)
    self.assertEqual(obj.to_natural(), natural)
    self.assertEqual(obj.to_lean(), lean)
    obj = cls.from_lean(lean, context)
    self.assertEqual(obj.to_natural(), natural)
    self.assertEqual(obj.to_lean(), lean)
