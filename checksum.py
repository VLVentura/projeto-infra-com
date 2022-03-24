def str_to_binary(message) -> str:
    return "".join(format(i, "08b") for i in bytearray(message, encoding="utf-8"))


def checksum(message) -> int:
    binary_message = str_to_binary(message)
    pass
