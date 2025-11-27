import sys

import pyfiglet

ascii_mapping = {chr(i): pyfiglet.figlet_format(chr(i), font='script', width=sys.maxsize) for i in range(32, 127)}

# add special cases to the mapping
for special in ('.)', '.}', '.p', ':p', '.j', ':j', ',b', '.b', '^^', '_4', '_~'):
    ascii_mapping[special] = pyfiglet.figlet_format(special, font='script', width=sys.maxsize)

# sort from biggest to smallest
ascii_mapping = dict(sorted(ascii_mapping.items(), key=lambda item: -len(item[1])))

def find_best_match(lines, mapping, last_char):
    best_matching_percent = 0.0
    best_match = ''
    best_total_characters = 0
    best_move_with = 0
    best_lines = None
    for move in range(0, 4):
        if best_matching_percent == 1.0 and best_move_with < move:
            if best_move_with == 0 and len(best_lines[0]) == 5:
                pass  # we can find a non-colliding thinner match which can be good for us
            else:
                break

        for charx, art in mapping.items():
            if charx == ' ' and move > 0:
                continue
            art_lines = art.splitlines()
            total_characters = 0
            matching_characters = 0
            for line1, line2 in zip(lines, art_lines):
                if charx != ' ':
                    line2 = line2.rstrip()
                total_characters += len(line2)
                matching_characters += max(0, sum(c1 == c2 for c1, c2 in zip(line1, ' ' * move + line2)) - move)

            assert total_characters > 0
            matching_percent = matching_characters / total_characters
            if matching_percent > best_matching_percent:
                best_matching_percent = matching_percent
                best_match = charx
                best_total_characters = total_characters
                best_move_with = move
                best_lines = art_lines
            elif matching_percent == best_matching_percent and best_matching_percent == 1.0:
                # if the art_lines and best_lines have common part -> prefer the more total characters
                has_common = False
                for l1, l2 in zip(art_lines, best_lines):
                    if any(c1 != ' ' and c2 != ' ' for c1, c2 in zip(' ' * (move - best_move_with) + l1, l2)):
                        has_common = True
                        break
                if has_common and total_characters < best_total_characters:
                    continue

                if has_common and total_characters == best_total_characters:
                    if best_match != ',' or charx != ':':  # this should be a ';', prefer :
                        print("ERROR")
                        assert False

                # if not has common part -> prefer the one with thinner shape by lines[0] count
                if not has_common and len(art_lines[0]) + move > len(best_lines[0]):
                    if best_move_with < move < 3 and charx == '/':
                        pass
                    elif move > best_move_with and charx != '_' and charx != '-' and charx != '=':
                        return best_match[0], best_move_with
                    else:
                        continue

                if not has_common and move > best_move_with and len(art_lines[0]) + move == len(best_lines[0]):
                    if charx == '/' and move < 3:
                        pass
                    else:
                        return best_match[0], best_move_with

                if not has_common and len(art_lines[0]) == len(best_lines[0]):
                    if '_' != charx:
                        print("ERROR")
                        assert False
                    elif best_match == '=' and last_char in "_hXLq":
                        pass
                    elif total_characters < best_total_characters:
                        continue

                best_match = charx
                best_total_characters = total_characters
                best_move_with = move
                best_lines = art_lines

    if best_matching_percent != 1.0:
        print('\n'.join(lines))
        print(f"Best match is '{best_match}' with {best_matching_percent * 100:.2f}% match.")
        print(mapping.get(best_match))
        raise ValueError("No perfect match found for the ascii art segment.")

    return best_match[0], best_move_with

# find original text from ascii art based on the mapping
def find_original_text(art, mapping=None):
    if mapping is None:
        mapping = ascii_mapping

    # Split the ascii art into lines
    lines = art.splitlines()
    # Initialize an empty string to store the original text
    original_text = ""
    try:
        while any(lines):
            # find 100% percent matching in mapping
            best_match, best_move_with = find_best_match(lines, mapping, (original_text or ' ')[-1])

            if best_match != ' ':
                original_text += best_match

                art_lines = mapping[best_match].splitlines()
                full_len = len(art_lines[0])

                # remove matched part from lines
                for en, line2 in enumerate(art_lines):
                    clear = len(line2.rstrip())
                    base = len(line2.strip())
                    lines[en] = lines[en][:clear - base + best_move_with] + ' ' * base + lines[en][
                        clear + best_move_with:]
            else:
                full_len = 0

            # remove empty columns from the left
            removed = 0
            while all(line.startswith(' ') for line in lines):
                lines = [line[1:] for line in lines]
                removed += 1

            if removed > full_len:
                original_text += ' ' * ((removed - full_len) // 2)

        return original_text
    except ValueError as e:
        # add original text found so far to the error message
        print(pyfiglet.figlet_format(original_text, font='script', width=sys.maxsize))
        raise ValueError(f"Partial recovered text: '{original_text}'") from e
    except AssertionError as e:
        # add original text found so far to the error message
        print(pyfiglet.figlet_format(original_text, font='script', width=sys.maxsize))
        raise ValueError(f"Partial recovered text: '{original_text}'") from e
