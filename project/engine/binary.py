import struct
from collections import OrderedDict


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


def encode_postings(postings, encoding=1):
    compressed = []

    last = 0
    for i in xrange(len(postings)):
        doc_id, freq = postings[i]
        if encoding == 1:
            code_id = vb_encode(doc_id)
        elif encoding == 2:
            code_id = gamma_encode(doc_id)
        else:
            code_id = doc_id

        new = (code_id, freq)
        compressed.append(new)
        last = doc_id
    
    return compressed


def _write_posting(file, p, encoding=1):
    doc_id, freq = p
    
    if encoding != 0:
        #ID
        fmt = '>' + 'B' * len(doc_id)
        data = struct.pack(fmt, *doc_id)
        file.write(data)

        #Freq
        data = struct.pack('>i', freq)
        file.write(data)
    else:
        data = struct.pack('>ii', doc_id, freq)
        file.write(data)


def _read_vb_code(file):
    byte_array = []

    while True:
        data = file.read(1) # Read byte
        byte = struct.unpack('B', data)[0]
        byte_array.append(byte)

        if to_byte_string(byte)[0] == '1':
            break

    return vb_decode(byte_array)


def _read_gamma_code(file):
    byte_array = []
    num_bits = 0

    end_unary = False
    while not end_unary:
        data = file.read(1) # Read byte
        byte = struct.unpack('B', data)[0]

        byte_string = to_byte_string(byte)
        byte_array.append(byte)

        for b in byte_string:
            if b == '1':
                num_bits += 1
            else:
                end_unary = True
                break

    rest = 8 - ((num_bits + 1) % 8)
    bits_needed = num_bits - rest
    bytes_needed = num_bytes_int(bits_needed)

    # Add bytes to complete the offset
    for i in xrange(bytes_needed):
        data = file.read(1) # Read byte
        byte = struct.unpack('B', data)[0]
        byte_array.append(byte)

    return gamma_decode(byte_array)


def write_index_binary(file, num_docs, index, encoding=1):
    for k, v in index.iteritems():
        index[k] = encode_postings(v)

    
    #N documents
    data = struct.pack('>i', num_docs)
    file.write(data)

    # Index type
    # 0 == Basic, 1 == Frequency, 2 == Positional
    data = struct.pack('B', 1)
    file.write(data)

    # Encoding
    # 0 == Uncompressed, 1 == Variable Byte, 2 == Gamma
    data = struct.pack('B', encoding)
    file.write(data)

    # N strings
    strings = [k for k in index.iterkeys()]
    num_strings = len(strings)
    data = struct.pack('>i', num_strings)
    file.write(data)

    for s in strings:
        # String length
        str_length = len(s)
        data = struct.pack('B', str_length)
        file.write(data)

        # String
        fmt = str(str_length) + 's'
        data = struct.pack(fmt, s)
        file.write(data)

        # N postings
        postings = index[s]
        num_postings = len(postings)
        data = struct.pack('>i', num_postings)
        file.write(data)

        # Postings
        for p in postings:
            _write_posting(file, p, encoding)

  
def read_index_binary(file):
    index = OrderedDict()

    # N documents
    data = file.read(4)
    num_docs = struct.unpack('>i', data)[0]

    # Index type
    # 0 == Basic, 1 == Frequency, 2 == Positional
    data = file.read(1)
    index_type = struct.unpack('B', data)[0]

    # Encoding
    # 0 == Uncompressed, 1 == Variable Byte, 2 == Gamma
    data = file.read(1)
    encoding = struct.unpack('B', data)[0]

    # N strings
    data = file.read(4)
    num_strings = struct.unpack('>i', data)[0]

    for i in xrange(num_strings):
        # String length
        data = file.read(1)
        str_length = struct.unpack('B', data)[0]

        # String
        fmt = str(str_length) + 's'
        data = file.read(str_length)
        string = struct.unpack(fmt, data)[0]
 
        # N postings
        data = file.read(4)
        num_postings = struct.unpack('>i', data)[0]

        # Postings
        postings = []
        for i in xrange(num_postings):
            #ID
            if encoding == 1:
                doc_id = _read_vb_code(file)
            elif encoding == 2:
                doc_id = _read_gamma_code(file)
            else:
                data = file.read(4)
                doc_id = struct.unpack('>i', data)[0]

            #Freq
            data = file.read(4)
            freq = struct.unpack('>i', data)[0]
            postings.append((doc_id, freq))

        index[string] = postings

    return num_docs, index
