import sys

from content_stream import get_book_body_stream

def main():
    # with open("books/calineczka.txt", "r", encoding="utf-8") as file:
    #     sys.stdout.write(get_book_body_stream(file).read())
    sys.stdout.write(get_book_body_stream(sys.stdin).read())

if __name__ == '__main__':
    main()