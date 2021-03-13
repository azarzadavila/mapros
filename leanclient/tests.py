from django.test import TestCase

# from https://github.com/leanprover-community/lean-client-python
from pathlib import Path

import trio  # type: ignore

from leanclient.trio_server import TrioLeanServer


async def main():
    lines = Path("leanclient/test.lean").read_text().split("\n")

    async with trio.open_nursery() as nursery:
        server = TrioLeanServer(nursery, debug=False)
        await server.start()
        await server.full_sync("leanclient/test.lean")

        for i, line in enumerate(lines):
            before = await server.state("leanclient/test.lean", i + 1, 0)
            after = await server.state("leanclient/test.lean", i + 1, len(line))
            if before or after:
                print(f"Line {i+1}: {line}")
                print(f"State before:\n{before}\n")
                print(f"State after:\n{after}\n")

        server.kill()
        nursery.cancel_scope.cancel()


class ExampleTest(TestCase):
    def test_basic(self):
        trio.run(main)
