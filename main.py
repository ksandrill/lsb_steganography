import argparse
from typing import Optional

import numpy as np
from PIL import Image

SRC = 'pictures_to_encode/Lenna.png'
OUT = 'pictures_to_decode/steg_Lenna.png'


def write_message_to_array(img_pixel_array: np.ndarray, binary_message: str) -> None:
    binary_message_size = len(binary_message)
    message_index = 0
    for i, pixel in enumerate(img_pixel_array):
        for j, channel_value in enumerate(pixel):
            if message_index < binary_message_size:
                binary_channel_value = format(channel_value, '08b')
                new_channel_value = (int(binary_channel_value[:-1] + binary_message[message_index], 2))
                img_pixel_array[i][j] = new_channel_value
                message_index += 1
            else:
                return


def encode_message(path_to_input_img: str, message: str, path_to_output_img: str, end_word: str = '$dafaq$') -> None:
    print('start encoding')
    img = Image.open(path_to_input_img, 'r')
    width, height = img.size
    img_pixel_array = np.array(list(img.getdata()))
    pixel_number, channels_number = img_pixel_array.shape
    message += end_word
    # convert message.txt to bits
    binary_message = ''.join([format(ord(i), "08b") for i in message])
    binary_message_size = len(binary_message)
    if binary_message_size > pixel_number:
        print('can''\'t encode message.txt cuz need ', binary_message_size - pixel_number, ' pixels to store data')
        return
    write_message_to_array(img_pixel_array, binary_message)
    img_pixel_array = img_pixel_array.reshape((height, width, channels_number))
    enc_img = Image.fromarray(img_pixel_array.astype('uint8'), img.mode)
    enc_img.save(path_to_output_img)
    print('encoded message.txt\n:', message[:-len(end_word)])


def decode_message(path_to_encoded_img: str, end_word: str = '$dafaq$') -> Optional[str]:
    print('start decoding')
    img = Image.open(path_to_encoded_img, 'r')
    img_pixel_array = np.array(list(img.getdata()))
    hidden_bits = []
    for pixel in img_pixel_array:
        for channel_value in pixel:
            binary_channel_value = format(channel_value, '08b')
            encoded_bit = binary_channel_value[-1]
            hidden_bits.append(encoded_bit)
    hidden_bytes = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]
    symbols_in_hidden_bytes = []
    message_is_found = False
    founded_message = ''
    end_word_len = len(end_word)
    for byte in hidden_bytes:
        char = chr(int((''.join(byte)), 2))
        symbols_in_hidden_bytes.append(char)
        if ''.join(symbols_in_hidden_bytes[-end_word_len:]) == end_word:
            message_is_found = True
            founded_message = ''.join(symbols_in_hidden_bytes[:-end_word_len])
            break
    if message_is_found:
        print('decoded message.txt\n: ' + founded_message)
        return founded_message

    else:
        print('no encoded messages here')
        return None


def main():
    message = []
    with open('messages_data/message.txt', 'r') as f:
        for line in f:
            message.append(line)
    message = ''.join(message)
    encode_message(SRC, message, OUT)
    founded_message = decode_message(OUT)
    if founded_message is not None:
        with open('messages_data/decoded_message.txt', 'w') as f:
            f.write(founded_message)


if __name__ == '__main__':
    main()
