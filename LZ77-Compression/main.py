from curses import window
from LZ77 import LZ77Compressor

compressor = LZ77Compressor(window_size=100)

input_file_path = './input.txt'
output_file_path = './compressed_file'

compressor.compress(input_file_path, output_file_path)
compressed_data = compressor.compress(input_file_path)

input_file_path = './compressed_file'
output_file_path = './decompressed_file.txt'

compressor.decompress(input_file_path, output_file_path)
decompressed_data = compressor.decompress(input_file_path)
