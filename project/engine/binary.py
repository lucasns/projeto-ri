def to_byte_string(i):
    binary = format(i, 'b')
    return binary.zfill(8)


def num_bytes(binary):
    return len(binary) / 8 + (len(binary) % 8 != 0)


def num_bytes_int(n):
    return n / 8 + (n % 8 != 0)


def unary(n):
    return '1' * n + '0'


def to_byte_array(binary_string):
    byte_array = []
    index = 0
    for i in xrange(num_bytes(binary_string)):
        byte = binary_string[index:index+8]
        byte_array.append(int(byte, 2))
        index = (i + 1) * 8

    return byte_array


def vb_encode(n):
    binary = format(n, 'b')
    num_bits = len(binary)

    code = ""

    while len(binary) > 0:
        if num_bits > 7:
            curr = binary[len(binary)-7: len(binary)]  # Last 7 bits
            code = curr.zfill(8) + code
            binary = binary[:len(binary)-7]  # Remove last 7 bits
            num_bits = len(binary)
        else:
            code = binary.zfill(8) + code
            binary = ""
            num_bits = len(binary)

    code = code[:len(code)-8] + '1' + code[len(code)-7:]
    byte_array = to_byte_array(code)
    return byte_array


def vb_decode(byte_array):
    binary = ""
    for byte in byte_array:
        binary = binary + to_byte_string(byte)[1:]

    return int(binary, 2)


def gamma_encode(n):
    binary = format(n, 'b')
    offset = binary[1:]
    unary_code = unary(len(offset))
    code =  unary_code + offset

    code = code.ljust(8 * num_bytes(code), '0') # Complete bytes
    byte_array = to_byte_array(code)

    return byte_array


def gamma_decode(byte_array):
    binary = ""
    for byte in byte_array:
        binary += to_byte_string(byte)

    offset_size = 0
    for b in binary:
        if b == '1':
            offset_size += 1
        else:
            break

    number = '1' + binary[offset_size + 1: 2 * offset_size + 1]
    return int(number, 2)
