#!/usr/bin/python

import os
import sys
import mmap
import struct
import contextlib
from argparse import ArgumentParser

def carveUsnRecords(inFile, outFile):
    with contextlib.closing(mmap.mmap(inFile.fileno(), 0, access=mmap.ACCESS_READ)) as m:
        offset = 0
        while True:
            offset = m.find(b'\x00\x00\x02\x00\x00\x00', offset)
            if offset == -1:
                break

            if m.find(b'\x00\x3c\x00', offset + 55, offset + 58) == -1:
                offset +=1
                continue

            offset -= 2
            recordLength = struct.unpack('<i', m[offset:offset + 4])[0]
            if recordLength < 62 or recordLength > 570:
                offset += 3
                continue

            outFile.write(m[offset:offset + recordLength])
            offset += (recordLength)

def main():
    p = ArgumentParser()
    p.add_argument("-f", "--file", help="Carve USN records from the given file", required=True)
    p.add_argument("-o", "--outfile", help="Output to the given file", required=True)
    args = p.parse_args()
    with open(args.file, "rb") as i:
        with open(args.outfile, "ab") as o:
            carveUsnRecords(i, o)


if __name__ == "__main__":
    main()
