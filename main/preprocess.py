import re


def char_slash_repl(match):
    return match[1] + " " + match[2]


def preprocess(nat: str):
    nat = nat.strip()
    nat = re.sub(r"\$\$", "", nat)
    nat = re.sub(r" +", " ", nat)
    nat = re.sub(r"\n+", "\n", nat)
    nat = re.sub(r"\r+", "\r", nat)
    nat = re.sub(r" *\n *", "\n", nat)
    nat = re.sub(r"([^\s\$])(\\)", char_slash_repl, nat)
    return nat
