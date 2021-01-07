import json
import os
from hashlib import sha256
from typing import Callable, Dict

H: Callable[[bytes], bytes] = lambda s: sha256(s).digest()


def get_mac(key: bytes, data: bytes) -> bytes:
    """Just a MAC generation function similar to HMAC.
    Reference link: https://en.wikipedia.org/wiki/HMAC#Implementation
    """
    if len(key) >= 32:
        key = H(key)

    if len(key) < 32:
        key += b"\x00" * (32 - len(key))

    inner_pad = bytearray(32)
    outer_pad = bytearray(32)
    for i in range(32):
        inner_pad[i] = key[i] ^ 0x20
        outer_pad[i] = key[i] ^ 0x21

    return H(outer_pad + H(inner_pad + data))


class SecureStorage:
    """Changes on data stored in this storage can be detected :) """

    def __init__(self, debug=False):
        self.keys: Dict[str, bytes] = {}  # key ID -> key
        self.data: Dict[bytes, bytes] = {}  # MAC -> data
        self.debug = debug
        if debug:
            # when debug mode is on, unique arguments to `store_data` will be
            # logged.
            self.store_data_args = set()

    def generate_key(self, key_id: str) -> None:
        """Generate a new key."""
        if key_id in self.keys:
            raise Exception("duplicated key id")
        self.keys[key_id] = os.urandom(32)

    def import_key(self, key_id: str, key: bytes) -> None:
        """Import an external key."""
        if key_id in self.keys:
            raise Exception("duplicated key id")
        self.keys[key_id] = key

    def store_data(self, key_id: str, data: bytes) -> bytes:
        """Store data and return a MAC that can be used to retrieve the data
        later."""
        if key_id not in self.keys:
            raise Exception("key not found")

        key = self.keys[key_id]
        if self.debug:
            self.store_data_args.add((key, data))

        mac = get_mac(key, data)
        if mac in self.data:
            raise Exception("data already stored")

        self.data[mac] = data
        return mac

    def retrieve_data(self, key_id: str, mac: bytes) -> bytes:
        """Retrieve data previously stored with `store_data`."""
        if key_id not in self.keys:
            raise Exception("key not found")
        if mac not in self.data:
            raise Exception("data not found")

        key = self.keys[key_id]
        data = self.data[mac]
        if get_mac(key, data) != mac:
            raise Exception("data has been tampered")
        return data

    def report_bug(self) -> int:
        """Claim your bounty here :) """
        if self.debug:
            # check for a massive collision bug
            if len(self.store_data_args) >= 10 and len(self.data) == 1:
                # check if collisions happened through different key sizes
                key_lengths = [len(key) for (key, _) in self.store_data_args]
                if min(key_lengths) < 32 <= max(key_lengths):
                    # Congrats :)
                    from secret import flag
                    return int.from_bytes(flag, "big")
        return 0


def main():
    ss = SecureStorage(debug=True)
    for _ in range(100):
        try:
            request = json.loads(input())

            if request["action"] == "generate_key":
                key_id = request["key_id"]
                ss.generate_key(key_id)
                print(json.dumps({}))

            if request["action"] == "import_key":
                key_id = request["key_id"]
                key = bytes.fromhex(request["key"])
                ss.import_key(key_id, key)
                print(json.dumps({}))

            elif request["action"] == "store_data":
                key_id = request["key_id"]
                data = bytes.fromhex(request["data"])
                mac = ss.store_data(key_id, data)
                print(json.dumps({"mac": mac.hex()}))

            elif request["action"] == "retrieve_data":
                key_id = request["key_id"]
                mac = bytes.fromhex(request["mac"])
                data = ss.retrieve_data(key_id, mac)
                print(json.dumps({"data": data.hex()}))

            elif request["action"] == "report_bug":
                print(json.dumps({"bounty": ss.report_bug()}))

        except EOFError:
            break
        except Exception as err:
            print(json.dumps({"error": str(err)}))


if __name__ == '__main__':
    main()
