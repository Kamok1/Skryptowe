# from typing import Generator, Tuple, TextIO
#
# from constants import EDITION_MARKER, NEW_LINE_SIGN, NUM_LINES_TO_CHECK
# from shared import clean_line, gen_lines
#
#
# def process_header(line_gen: Generator[str, None, None], edition_marker: str, new_line_sign: str, num_lines_to_check: int) -> Tuple[str, bool]:
#     header_buffer = ""
#     preamble_detected = False
#     is_prev_blank = False
#     line_count = 0
#
#     for line in line_gen:
#         cleaned = clean_line(line)
#         if cleaned.startswith(edition_marker):
#             return "", False
#
#         header_buffer += cleaned + new_line_sign
#         line_count += 1
#
#         if cleaned != "":
#             is_prev_blank = False
#         else:
#             if is_prev_blank:
#                 preamble_detected = True
#                 break
#             else:
#                 is_prev_blank = True
#
#         if line_count >= num_lines_to_check:
#             break
#
#     return header_buffer, preamble_detected
#
# def process_body(line_gen: Generator[str, None, None], edition_marker: str, new_line_sign: str) -> Generator[str, None, None]:
#     first_line = True
#     for line in line_gen:
#         cleaned = clean_line(line)
#         if cleaned.startswith(edition_marker):
#             return
#         if not first_line:
#             yield new_line_sign
#         yield cleaned
#         first_line = False
#
#
# def extract_book_text(stream: TextIO, edition_marker: str = EDITION_MARKER,new_line_sign: str = NEW_LINE_SIGN, num_lines_to_check: int = NUM_LINES_TO_CHECK) -> str:
#     line_gen = gen_lines(stream)
#     header_buffer, is_preamble_detected = process_header(line_gen, edition_marker, new_line_sign, num_lines_to_check)
#     output = "" if is_preamble_detected else header_buffer
#     output += "".join(process_body(line_gen, edition_marker, new_line_sign))
#     return output
