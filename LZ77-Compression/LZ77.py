from bitarray import bitarray


class LZ77Compressor:

    MAX_WINDOW_SIZE = 400

    def __init__(self, window_size=20):
        self.window_size = min(window_size, self.MAX_WINDOW_SIZE)
        self.lookahead_buffer_size = 15

    def compress(self, input_file_path, output_file_path=None):
        data = None
        i = 0
        output_buffer = bitarray(endian='big')

        try:
            with open(input_file_path, 'rb') as input_file:
                data = input_file.read()
        except IOError:
            print('Could not open input file ...')
            raise

        while i < len(data):
            match = self.findLongestMatch(data, i)

            if match:
                (bestMatchDistance, bestMatchLength) = match

                output_buffer.append(True)
                output_buffer.frombytes(bytes([bestMatchDistance >> 4]))
                output_buffer.frombytes(
                    bytes([((bestMatchDistance & 0xf) << 4) | bestMatchLength]))
                print(f"<1, {bestMatchDistance}, {bestMatchLength}>")

                i += bestMatchLength
            else:
                output_buffer.append(False)
                output_buffer.frombytes(bytes([data[i]]))
                print(f"<0, {chr(data[i])}>")
                i += 1

        output_buffer.fill()
        if output_file_path:
            try:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(output_buffer.tobytes())
                    print(
                        "File was compressed successfully and saved to output path ...")
                    return None
            except IOError:
                print(
                    'Could not write to output file path. Please check if the path is correct ...')
                raise
        return output_buffer

    def decompress(self, input_file_path, output_file_path=None):
        data = bitarray(endian='big')
        output_buffer = []

        try:
            with open(input_file_path, 'rb') as input_file:
                data.fromfile(input_file)
        except IOError:
            print('Could not open input file ...')
            raise

        while len(data) >= 9:

            flag = data.pop(0)

            if not flag:
                byte = data[0:8].tobytes()

                output_buffer.append(byte)
                del data[0:8]
            else:
                byte1 = ord(data[0:8].tobytes())
                byte2 = ord(data[8:16].tobytes())

                del data[0:16]
                distance = (byte1 << 4) | (byte2 >> 4)
                length = (byte2 & 0xf)

                for _ in range(length):
                    output_buffer.append(output_buffer[-distance])
        out_data = b''.join(output_buffer)

        if output_file_path:
            try:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(out_data)
                    print(
                        'File was decompressed successfully and saved to output path ...')
                    return None
            except IOError:
                print(
                    'Could not write to output file path. Please check if the path is correct ...')
                raise
        return out_data

    def findLongestMatch(self, data, current_position):
        end_of_buffer = min(current_position +
                            self.lookahead_buffer_size, len(data) + 1)

        best_match_distance = -1
        best_match_length = -1

        for j in range(current_position + 2, end_of_buffer):

            start_index = max(0, current_position - self.window_size)
            substring = data[current_position:j]

            for i in range(start_index, current_position):

                repetitions = len(substring) // (current_position - i)

                last = len(substring) % (current_position - i)

                matched_string = data[i:current_position] * \
                    repetitions + data[i:i+last]

                if matched_string == substring and len(substring) > best_match_length:
                    best_match_distance = current_position - i
                    best_match_length = len(substring)

        if best_match_distance > 0 and best_match_length > 0:
            return (best_match_distance, best_match_length)
        return None
