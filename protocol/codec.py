# protocol/codec.py

class ProtocolError(Exception):
    pass

def decode_line(line: str):
    line = line.strip()

    if not line.startswith("|") or not line.endswith("|"):
        raise ProtocolError("Bad framing")

    parts = line.split("|")[1:-1]

    if len(parts) == 0:
        raise ProtocolError("Empty message")

    op = parts[0].upper()
    fields = parts[1:]

    return op, fields


def encode(op, *fields):
    return "|" + "|".join([op] + [str(f) for f in fields]) + "|\n"
