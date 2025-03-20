import sys
from typing import TextIO


def get_non_whitespace_count(stream: TextIO) -> int:
    count = 0
    for line in stream:
        for char in line:
            if not char.isspace():
                count += 1
    return count

def main():

    count = get_non_whitespace_count(sys.stdin)
    sys.stdout.write(str(count))

if __name__ == '__main__':
    main()
