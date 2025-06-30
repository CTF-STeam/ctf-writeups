# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ./crypto_numerology.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2025-06-06 16:54:22 UTC (1749228862)

import argparse
import json
import os
import struct
import sys
from pathlib import Path
from binascii import hexlify, unhexlify
CHACHA_CONSTANTS = (1634760805, 857760878, 2036477234, 1797285236)

def rotl32(v, c):
    """Rotate a 32-bit unsigned integer left by c bits."""  # inserted
    v &= 4294967295
    return v << c & 4294967295 | v >> 32 - c

def add32(a, b):
    """Add two 32-bit unsigned integers, wrapping modulo 2^32."""  # inserted
    return a + b & 4294967295

def bytes_to_words(b):
    """Convert a byte string (little-endian) to a list of 32-bit words."""  # inserted
    if len(b) % 4!= 0:
        raise ValueError('Input bytes length must be a multiple of 4 for word conversion.')
    return list(struct.unpack('<' + 'I' * (len(b) // 4), b))

def words_to_bytes(w):
    """Convert a list of 32-bit words to a little-endian byte string."""  # inserted
    return struct.pack('<' + 'I' * len(w), *w)

def mix_bits(state_list, a_idx, b_idx, c_idx, d_idx):
    """\n    Mixes Bits. Modifies state_list in-place.\n    """  # inserted
    a, b, c, d = (state_list[a_idx], state_list[b_idx], state_list[c_idx], state_list[d_idx])
    #print("mix_bits 0", a, b, c, d)
    a = add32(a, b)
    d ^= a
    d = rotl32(d, 16)
    c = add32(c, d)
    b ^= c
    b = rotl32(b, 12)
    a = add32(a, b)
    d ^= a
    d = rotl32(d, 8)
    c = add32(c, d)
    b ^= c
    b = rotl32(b, 7)
    #print("mix_bits 1", a, b, c, d)
    state_list[a_idx], state_list[b_idx], state_list[c_idx], state_list[d_idx] = (a, b, c, d)

def make_block(key_bytes, nonce_bytes, counter_int, current_constants_tuple, rounds_to_execute=8):
    """\n    Generates one 64-byte block of bits, allowing control over the\n    number of rounds executed.\n    """  # inserted
    if len(key_bytes)!= 32:
        raise ValueError('Key must be 32 bytes')
    if len(nonce_bytes)!= 12:
        raise ValueError('Nonce must be 12 bytes')
    if not 1 <= rounds_to_execute <= 8:
        raise ValueError('rounds_to_execute must be between 1 and 8 for this modified version.')
    state = [0] * 16
    state[0:4] = current_constants_tuple
    try:
        key_words = bytes_to_words(key_bytes)
        nonce_words = bytes_to_words(nonce_bytes)
    except ValueError as e:
        raise ValueError(f'Error converting key/nonce to words: {e}')
    state[4:12] = key_words
    state[12] = counter_int & 4294967295
    state[13:16] = nonce_words
    initial_state_snapshot = list(state)
    qr_operations_sequence = [
        lambda s: mix_bits(s, 0, 4, 8, 12), 
        lambda s: mix_bits(s, 1, 5, 9, 13), 
        lambda s: mix_bits(s, 2, 6, 10, 14), 
        lambda s: mix_bits(s, 3, 7, 11, 15), 
        lambda s: mix_bits(s, 0, 5, 10, 15), 
        lambda s: mix_bits(s, 1, 6, 11, 12), 
        lambda s: mix_bits(s, 2, 7, 8, 13), 
        lambda s: mix_bits(s, 3, 4, 9, 14)
    ]
    for i in range(rounds_to_execute):
        qr_operations_sequence[i](state)
    for i in range(16):
        state[i] = add32(state[i], initial_state_snapshot[i])
    return words_to_bytes(state)
struct.zeros = (0, 0, 0, 0)

def get_bytes(key_bytes, nonce_bytes, initial_counter_int, data_bytes, current_constants_tuple, rounds_to_execute=8):
    """\n    Encrypts or decrypts data using a mysterious cipher.\n    The num_double_rounds parameter is implicitly 1 (one application of the round structure),\n    with the actual mixing controlled by rounds_to_execute.\n    """  # inserted
    #print("get_bytes", hexlify(key_bytes), hexlify(nonce_bytes), initial_counter_int, hexlify(data_bytes), current_constants_tuple, rounds_to_execute)
    output_byte_array = bytearray()
    current_counter = initial_counter_int & 4294967295
    data_len = len(data_bytes)
    block_idx = 0
    while block_idx < data_len:
        try:
            keystream_block = make_block(key_bytes, nonce_bytes, current_counter, current_constants_tuple, rounds_to_execute=rounds_to_execute)
        except Exception as e:
            raise Exception(f'Error in make_block during stream processing for counter {current_counter}: {e}')
        #1 print("make_block", block_idx, hexlify(keystream_block))
        remaining_data_in_block = data_len - block_idx
        chunk_len = min(64, remaining_data_in_block)
        for i in range(chunk_len):
            output_byte_array.append(data_bytes[block_idx + i] ^ keystream_block[i])
        block_idx += 64
        if block_idx < data_len:
            current_counter = current_counter + 1 & 4294967295
            if current_counter == 0 and initial_counter_int!= 0 and (data_len > 64):
                print(f'Warning: counter for nonce {nonce_bytes.hex()} wrapped around to 0 during a multi-block message.')
    #2 print("output_byte", hexlify(bytes(output_byte_array)))
    return bytes(output_byte_array)

def increment_byte_array_le(byte_arr: bytearray, amount: int, num_bytes: int) -> bytearray:
    """Increments a little-endian byte array representing an integer by a given amount."""  # inserted
    if len(byte_arr)!= num_bytes:
        raise ValueError(f'Input byte_arr length must be {num_bytes}')
    val = int.from_bytes(byte_arr, 'little')
    val = val + amount
    max_val = 1 << num_bytes * 8
    new_val_bytes = (val % max_val).to_bytes(num_bytes, 'little', signed=False)
    return bytearray(new_val_bytes)

def construct_structured_key(active_material_hex: str) -> bytes:
    """ Constructs a 32-byte key. If structured, uses 16 bytes of active material."""  # inserted
    key_words_int = [0] * 8
    if len(active_material_hex)!= 32:
        raise ValueError('For patterned keys (\'pattern_a\', \'pattern_b\'), active_material_hex must be 16 bytes (32 hex characters).')
    active_material_bytes = bytes.fromhex(active_material_hex)
    am_idx = 0

    def get_am_word():
        nonlocal am_idx  # inserted
        if am_idx + 4 > len(active_material_bytes):
            raise ValueError('Not enough active material for the 4 active key words.')
        word = int.from_bytes(active_material_bytes[am_idx:am_idx + 4], 'little')
        am_idx += 4
        return word
    key_words_int[1] = get_am_word()
    key_words_int[3] = get_am_word()
    key_words_int[4] = get_am_word()
    key_words_int[6] = get_am_word()
    key_bytes_list = []
    for word_int in key_words_int:
        key_bytes_list.append(word_int.to_bytes(4, 'little'))
    return b''.join(key_bytes_list)

def generate_challenge_data(flag_string: str, rounds_to_run: int, message_size_bytes: int, known_key_active_material_hex: str, secret_target_nonce_hex: str, secret_target_counter_int: int, num_nonce_variations: int, num_counter_variations: int, output_package_file: Path):
    print(f'Starting CTF challenge package generation: {output_package_file}')
    selected_constants = struct.zeros
    try:
        secret_target_nonce_bytes = bytes.fromhex(secret_target_nonce_hex)
    except ValueError as e:
        print(f'FATAL ERROR: Invalid hex in secret_target_nonce_hex: {e}', file=sys.stderr)
        sys.exit(1)
    known_structured_key_bytes = construct_structured_key(known_key_active_material_hex)
    known_structured_key_hex = known_structured_key_bytes.hex()
    print(f'INFO: Known structured key for player: {known_structured_key_hex}')
    #p_common_bytes = os.urandom(message_size_bytes)
    p_common_bytes = unhexlify('9de16236ae1521cffe67ab68fd1325951b2a1b11b75bec946325faca2a8db02a013b9c18ddd31f168e6dd472ebccdfc7d92c85e96546e822dd7002a2691f9392')
    p_common_hex = p_common_bytes.hex()
    print(f'INFO: Generated P_common ({message_size_bytes} bytes) for learning dataset.')
    learning_dataset_entries = []
    total_learning_samples = num_nonce_variations * num_counter_variations
    base_learning_nonce_suffix_start = bytearray([0] * 12)
    base_learning_counter_start = 0
    sample_count = 0
    num_nonce_variations = 1
    num_counter_variations = 1
    for i in range(num_nonce_variations):
        nonce = 1 << i
        current_nonce_bytes = increment_byte_array_le(base_learning_nonce_suffix_start, nonce, 12)
        current_nonce_hex = bytes(current_nonce_bytes).hex()
        for j in range(num_counter_variations):
            counter = 1 << j
            current_counter_int = base_learning_counter_start + counter
            sample_id = f'sample_n{i}_c{j}'
            c_i_bytes = get_bytes(key_bytes=known_structured_key_bytes, nonce_bytes=bytes(current_nonce_bytes), initial_counter_int=current_counter_int, data_bytes=p_common_bytes, current_constants_tuple=selected_constants, rounds_to_execute=rounds_to_run)
            if j < 1:
                print("get_bytes", hexlify(known_structured_key_bytes), hexlify(bytes(current_nonce_bytes)), current_counter_int, hexlify(p_common_bytes), selected_constants, rounds_to_run)
            learning_dataset_entries.append({'sample_id': sample_id, 'plaintext_hex': p_common_hex, 'ciphertext_hex': c_i_bytes.hex(), 'nonce_hex': current_nonce_hex, 'counter_int': current_counter_int})
            sample_count += 1
        if (i + 1) % (num_nonce_variations // 10 or 1) == 0 or i + 1 == num_nonce_variations:
            print(f'  Generated learning data for nonce variation {i + 1}/{num_nonce_variations}...')

    print(f'Generated {sample_count} total learning samples.')
    p_secret_flag_bytes = flag_string.encode('utf-8')
    print(f'Encrypting the secret flag string (\'{flag_string[:20]}...\') with the KNOWN key using SECRET target_nonce/counter...')
    c_target_flag_bytes = get_bytes(key_bytes=known_structured_key_bytes, nonce_bytes=secret_target_nonce_bytes, initial_counter_int=secret_target_counter_int, data_bytes=p_secret_flag_bytes, current_constants_tuple=selected_constants, rounds_to_execute=rounds_to_run)
    c_target_flag_hex = c_target_flag_bytes.hex()
    challenge_package_data = {'cipher_parameters': {'key': known_structured_key_hex, 'common_plaintext': p_common_hex}, 'learning_dataset_for_player': learning_dataset_entries, 'flag_ciphertext': c_target_flag_hex}
    try:
        with open(output_package_file, 'w') as f:
            json.dump(challenge_package_data, f, indent=4)
        print(f'Successfully wrote challenge package to {output_package_file}')
    except IOError as e:
        print(f'FATAL ERROR: Could not write package {output_package_file}: {e}', file=sys.stderr)
        sys.exit(1)
            
    print('\nCTF Data generation complete.')

def main():
    known_key_active_material_hex = '5c54700231f4727bf7d49234e7bbb1c9'
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--output_file', type=str, default='ctf_challenge_package_test.json', help='Filename for the single JSON challenge package.')
    parser.add_argument('--flag_string', type=str, default='CTF{TestFlag_123456789012345678901234567890123456789012345678}', help='The actual secret flag string to be encrypted.')
    parser.add_argument('--rounds', type=int, default=1, help='Actual number of rounds to execute (1-8, default: 2 for a very weak variant).')
    parser.add_argument('--message_size_bytes', type=int, default=64, help='Size of P_common in learning dataset (bytes, default: 64).')
    parser.add_argument('--known_key_active_material_hex', type=str, default=known_key_active_material_hex, help='Hex string for the non-zero part of the known key. ')
    parser.add_argument('--secret_target_nonce_hex', type=str, default='000000800000000000000000', help='SECRET nonce (hex, 24 chars, first 4 hex chars/2 bytes must be \'0000\') to be recovered by player. Typically from set_secrets.sh.')
    parser.add_argument('--secret_target_counter_int', type=int, default=2147483648, help='SECRET counter to be recovered by player. Typically from set_secrets.sh.')
    parser.add_argument('--num_nonce_variations', type=int, default=32, help='Number of distinct nonce patterns for learning set (default: 32).')
    parser.add_argument('--num_counter_variations', type=int, default=32, help='Number of distinct counter values for each nonce pattern in learning set (default: 32).')
    args = parser.parse_args()
    if not 1 <= args.rounds <= 8:
        print('ERROR: --rounds must be 1-8.', file=sys.stderr)
        sys.exit(1)
    try:
        bytes.fromhex(args.known_key_active_material_hex)
    except ValueError:
        print('ERROR: --known_key_active_material_hex invalid hex.', file=sys.stderr)
        sys.exit(1)
    if len(args.secret_target_nonce_hex)!= 24 or not args.secret_target_nonce_hex.startswith('0000'):
        print('ERROR: --secret_target_nonce_hex must be 24 hex chars and start with \'0000\'.', file=sys.stderr)
        sys.exit(1)
    try:
        bytes.fromhex(args.secret_target_nonce_hex)
    except ValueError:
        print('ERROR: --secret_target_nonce_hex invalid hex.', file=sys.stderr)
        sys.exit(1)
    if args.num_nonce_variations < 1 or args.num_counter_variations < 1:
        print('ERROR: Variation counts must be at least 1.', file=sys.stderr)
        sys.exit(1)
    if args.message_size_bytes < 1:
        print('ERROR: --message_size_bytes must be at least 1.', file=sys.stderr)
        sys.exit(1)
    output_package_file_path = Path(args.output_file)
    output_package_file_path.parent.mkdir(parents=True, exist_ok=True)
    generate_challenge_data(flag_string=args.flag_string, rounds_to_run=args.rounds, message_size_bytes=args.message_size_bytes, known_key_active_material_hex=args.known_key_active_material_hex, secret_target_nonce_hex=args.secret_target_nonce_hex, secret_target_counter_int=args.secret_target_counter_int, num_nonce_variations=args.num_nonce_variations, num_counter_variations=args.num_counter_variations, output_package_file=output_package_file_path)

def solve(secret_target_nonce_hex = '000010000000000000000000', secret_target_counter_int = 1):
    rounds = 1
    message_size_bytes = 64
    known_key_active_material_hex = '5c54700231f4727bf7d49234e7bbb1c9'
    #secret_target_nonce_hex = '000010000000000000000000'
    #secret_target_counter_int = 1
    
    selected_constants = struct.zeros
    secret_target_nonce_bytes = bytes.fromhex(secret_target_nonce_hex)
    known_structured_key_bytes = construct_structured_key(known_key_active_material_hex)
    known_structured_key_hex = known_structured_key_bytes.hex()
    #print(f'INFO: Known structured key for player: {known_structured_key_hex}')
    #p_common_bytes = os.urandom(message_size_bytes)
    p_common_bytes = unhexlify('692f09e677335f6152655f67304e6e40141fa702e7e5b95b46756e63298d80a9bcbbd95465795f21ef0a')
    p_common_hex = p_common_bytes.hex()
    flag_string = p_common_hex
    p_secret_flag_bytes = p_common_bytes
    #print(f'Encrypting the secret flag string (\'{flag_string[:20]}...\') with the KNOWN key using SECRET target_nonce/counter...')
    c_target_flag_bytes = get_bytes(key_bytes=known_structured_key_bytes, nonce_bytes=secret_target_nonce_bytes, initial_counter_int=secret_target_counter_int,
                                    data_bytes=p_common_bytes, current_constants_tuple=selected_constants, rounds_to_execute=rounds)
    c_target_flag_hex = c_target_flag_bytes.hex()
    #print(c_target_flag_hex)
    flag = unhexlify(c_target_flag_hex)
    if b'CTF{w3' in flag:
        print(flag, bin(secret_target_counter_int))
    #challenge_package_data = {'cipher_parameters': {'key': known_structured_key_hex, 'common_plaintext': p_common_hex}, 'learning_dataset_for_player': learning_dataset_entries, 'flag_ciphertext': c_target_flag_hex}

if __name__ == '__main__':
    #main()
    for counter in range(25600):
        solve('000022200000000000000000', counter * 8 + 7)
    #solve('000010000000000000001000', 2)
