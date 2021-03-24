from pathlib import Path

import trio
import os

from leanclient.commands import Severity
from leanclient.trio_server import TrioLeanServer

LEAN_DIR = "lean-project/"
LEAN_DIR_SRC = LEAN_DIR + "src/"


def chdir():
    cur = os.getcwd()
    os.chdir(LEAN_DIR)
    return cur


def get_error(messages):
    for msg in messages:
        if msg.severity == Severity.error:
            return msg.text
    return None


async def states_lines_async(path, lines):
    tot_lines = Path(path).read_text(encoding="utf-8").split("\n")
    res = []
    async with trio.open_nursery() as nursery:
        server = TrioLeanServer(nursery)
        await server.start()
        with trio.move_on_after(10):
            await server.full_sync(path)
        for i in range(len(lines)):
            after = await server.state(path, lines[i], len(tot_lines[lines[i] - 1]))
            res.append(after)
        err = get_error(server.messages)
        server.kill()
        nursery.cancel_scope.cancel()
    return res, err


def states(path, lines):
    old_dir = chdir()
    path = "src/" + path
    try:
        res, err = trio.run(states_lines_async, path, lines)
    finally:
        os.chdir(old_dir)
    return res, err
