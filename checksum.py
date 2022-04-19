def padding(messages) -> bytearray:
    tempARR = []
    paddingArr = bytearray(str(messages),encoding="utf-8")
    tempARR.append(paddingArr)
    tempARR.insert(0,bytearray(str("0"*((-len(paddingArr))%16)),encoding="utf-8")) #add padding to data
    newArr = bytearray(tempARR[0]) + bytearray(tempARR[1])
    return newArr
def str_to_binary(messages: list) -> list:
    binary_messages = []
    for i in range(len(messages)):
        binary_messages.append("".join(format(padding(messages[i]), "08b")))
    return binary_messages


def checksum(message: list) -> str:
    var = str_to_binary(message)
    var2 = [ord("0") for _ in range(len(var[0]))]

    for i in range(len(var)):
        for j in range(len(var[i])):
            var2[j] += ord(var[i][j])

    for i in range(len(var2)):
        if i < len(var2):
            resto = var2[i] % 48
            if resto == 0:
                var2[i] = ord("0")
            if resto == 1:
                var2[i] = ord("1")
            if resto == 2:
                var2[i] = ord("1")
                var2[(i + 1)] += ord("1")

        if i == len(var2):
            resto = var2[i] % 48
            if resto == 0:
                var2[i] = ord("0")
            if resto == 1:
                var2[i] = ord("1")
            if resto == 2:
                var2[i] = ord("1")
                var2[0] += ord("1")

    for i in range(len(var2)):
        if i < len(var2):
            resto = var2[i] % 48
            if resto == 0:
                var2[i] = ord("0")
            if resto == 1:
                var2[i] = ord("1")
            if resto == 2:
                var2[i] = ord("1")
                var2[(i + 1)] += ord("1")

        if i == len(var2):
            resto = var2[i] % 48
            if resto == 0:
                var2[i] = ord("0")
            if resto == 1:
                var2[i] = ord("1")
            if resto == 2:
                var2[i] = ord("1")
                var2[0] += ord("1")

    for i in range(len(var2)):
        var2[i] = var2[i] // ord("1")

    for i in range(len(var2)):
        if var2[i] == 0:
            var2[i] = 1
        else:
            var2[i] = 0

    return "".join([str(x) for x in var2])
