from web3 import Web3


def add_zero_padding_to_hex(hex_string: str, num_of_bytes: int):
    return f"0x{hex_string[2:].zfill(num_of_bytes * 2)}"


def remove_decimals(value: int) -> int:
    return Web3.to_wei(value, "ether")
