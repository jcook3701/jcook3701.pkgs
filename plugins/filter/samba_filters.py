#!/usr/bin/python3
#
# samba_filters.py for jcook3701.pkgs
#
# SPDX-FileCopyrightText: Jared Cook
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import struct
from collections.abc import Callable
from typing import Any

DOCUMENTATION = """
    name: to_ntlm
    author: Jared Cook (jcook3701)
    version_added: "1.0.0"
    short_description: Convert a plaintext password into an NTLM MD4 hash.
    description:
        - This filter accepts a plaintext password string input, encodes it to
          UTF-16LE, and generates a 32-character upper-case NTLM MD4 hash string.
        - Designed explicitly to populate sambaNTPassword attributes inside OpenLDAP.
    positional_arguments_description:
        - password: The plaintext input password string to convert.
    requirements:
        - hashlib (standard Python library)
        - struct (standard Python library)
"""


def _f(x: int, y: int, z: int) -> int:
    """MD4 Round 1 conditional function."""
    return (x & y) | (~x & z)


def _g(x: int, y: int, z: int) -> int:
    """MD4 Round 2 conditional function."""
    return (x & y) | (x & z) | (y & z)


def _h(x: int, y: int, z: int) -> int:
    """MD4 Round 3 conditional function."""
    return x ^ y ^ z


def _rot(val: int, r: int) -> int:
    """Bitwise left rotation bounded to 32-bits."""
    return ((val << r) | (val >> (32 - r))) & 0xFFFFFFFF


def _md4_pure_python(data: bytes) -> str:
    """Compute an MD4 hash using a pure-Python implementation.
    This bypasses strict host OpenSSL configurations that block MD4.
    """
    # Padding the input bytes
    orig_len = len(data)
    padded_data = bytearray(data)
    padded_data.append(0x80)
    while (len(padded_data) % 64) != 56:
        padded_data.append(0x00)
    padded_data.extend(struct.pack("<Q", orig_len * 8))

    # Initialize variables
    h0, h1, h2, h3 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

    # Process 64-byte chunks
    for offset in range(0, len(padded_data), 64):
        x = list(struct.unpack("<16I", padded_data[offset : offset + 64]))
        a, b, c, d = h0, h1, h2, h3

        # Round 1
        for i in range(0, 16, 4):
            a = _rot((a + _f(b, c, d) + x[i]) & 0xFFFFFFFF, 3)
            d = _rot((d + _f(a, b, c) + x[i + 1]) & 0xFFFFFFFF, 7)
            c = _rot((c + _f(d, a, b) + x[i + 2]) & 0xFFFFFFFF, 11)
            b = _rot((b + _f(c, d, a) + x[i + 3]) & 0xFFFFFFFF, 19)

        # Round 2
        for i in range(4):
            a = _rot((a + _g(b, c, d) + x[i] + 0x5A827999) & 0xFFFFFFFF, 3)
            d = _rot((d + _g(a, b, c) + x[i + 4] + 0x5A827999) & 0xFFFFFFFF, 5)
            c = _rot((c + _g(d, a, b) + x[i + 8] + 0x5A827999) & 0xFFFFFFFF, 9)
            b = _rot((b + _g(c, d, a) + x[i + 12] + 0x5A827999) & 0xFFFFFFFF, 13)

        # Round 3
        for i in (0, 2, 1, 3):
            a = _rot((a + _h(b, c, d) + x[i] + 0x6ED9EBA1) & 0xFFFFFFFF, 3)
            d = _rot((d + _h(a, b, c) + x[i + 8] + 0x6ED9EBA1) & 0xFFFFFFFF, 9)
            c = _rot((c + _h(d, a, b) + x[i + 4] + 0x6ED9EBA1) & 0xFFFFFFFF, 11)
            b = _rot((b + _h(c, d, a) + x[i + 12] + 0x6ED9EBA1) & 0xFFFFFFFF, 15)

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF

    return struct.pack("<4I", h0, h1, h2, h3).hex().upper()


def to_ntlm(password: Any) -> str:
    """Convert a plaintext password into an upper-case NTLM MD4 hash.

    Args:
        password: The plaintext input password string.

    Returns:
        The computed 32-character hexadecimal NTLM MD4 string.
    """
    if not password:
        return ""

    encoded_bytes: bytes = str(password).encode("utf-16le")
    return _md4_pure_python(encoded_bytes)


class FilterModule:
    """Ansible FilterModule interface for registration within Jinja2 engines."""

    def filters(self) -> dict[str, Callable[[Any], str]]:
        """Register custom filter string mappings to Python functions.

        Returns:
            A dictionary mapping Jinja2 filter names to their handler functions.
        """
        return {"to_ntlm": to_ntlm}


if __name__ == "__main__":
    # Test vectors: (Plaintext, Correct NTLM Hash)
    test_cases = [
        ("SecurePass2026!", "43CA918443683917E88F7C481675F40F"),
        ("Admin_Samba_99", "DFCE12EEF45AD8E6367B5862AFB95838"),
        ("k3rb3ros_Ldap#", "4C9271F27355B398B248380723E4194B"),
        ("Net_Share_Game_84", "0D8DFE9FE73884AC0D65EB092F600865"),
        ("Infra_CEO_JCook3", "8F17E37B7D96B0E55ED0D88DB4EB5437"),
    ]

    print("--- Running NTLM Filter Verification ---")
    all_passed = True

    for plaintext, expected in test_cases:
        calculated = to_ntlm(plaintext)
        if calculated == expected:
            print(f"✅ PASSED: '{plaintext}' -> {calculated}")
        else:
            print(f"❌ FAILED: '{plaintext}'")
            print(f"   Calculated: {calculated}")
            print(f"   Expected:   {expected}")
            all_passed = False

    if all_passed:
        print("\n🎉 Success! Byte-packing logic matches NTLM standards.")
