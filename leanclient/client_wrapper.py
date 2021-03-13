from pathlib import Path

import trio
import os

from leanclient.trio_server import TrioLeanServer

LEAN_DIR = "lean-project/"
LEAN_DIR_SRC = LEAN_DIR + "src/"


def chdir():
    cur = os.getcwd()
    os.chdir(LEAN_DIR)
    return cur


async def states_lines_async(path, lines):
    tot_lines = Path(path).read_text().split("\n")
    res = []
    async with trio.open_nursery() as nursery:
        server = TrioLeanServer(nursery)
        await server.start()
        await server.full_sync(path)
        for i in range(len(lines)):
            after = await server.state(path, lines[i], len(tot_lines[lines[i] - 1]))
            res.append(after)
        server.kill()
        nursery.cancel_scope.cancel()
    return res


def states(path, lines):
    old_dir = chdir()
    path = "src/" + path
    try:
        res = trio.run(states_lines_async, path, lines)
    finally:
        os.chdir(old_dir)
    return res
