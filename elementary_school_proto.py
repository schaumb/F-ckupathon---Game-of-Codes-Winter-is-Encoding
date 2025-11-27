import random
import sys

import pyfiglet
from reverse_figlet import find_original_text

digits = ["""        
/      \\
|      |
|      |
|      |
\\------/
        """, """        
/      \\
|      |
|  X  |
|      |
\\------/
        ""","""        
/      \\
|    X|
|      |
|X    |
\\------/
        ""","""        
/      \\
|    X|
|  X  |
|X    |
\\------/
        ""","""        
/      \\
|X  X|
|      |
|X  X|
\\------/
        ""","""        
/      \\
|X  X|
|  X  |
|X  X|
\\------/
        ""","""        
/      \\
|X  X|
|X  X|
|X  X|
\\------/
        ""","""        
/      \\
|X  X|
|XXX|
|X  X|
\\------/
        ""","""        
/      \\
|XXX|
|X  X|
|XXX|
\\------/
        ""","""        
/      \\
|XXX|
|XXX|
|XXX|
\\------/
        """]

az = 'X' + ("  \n" * 10000)[2:]

fruits = "🍎🍌🍊🍓🍇🍉🍒🍐🍑🍋🥝🥭🫐🍈🍍"

def _addTo(orig, new):
    orig_lines = orig.splitlines()
    new_lines = new.splitlines()
    result_lines = []
    for o_line, n_line in zip(orig_lines, new_lines):
        result_lines.append(o_line + n_line)
    return '\n'.join(result_lines)

def serialize(any_obj):
    if isinstance(any_obj, int):
        result = '\n' * 7
        the_type = '🔢'
        # return pyfiglet.figlet_format(str(any_obj), font='script', width=sys.maxsize)

        fruitIndex = 0
        digit_arts = []
        if any_obj == 0:
            digit_arts.append(digits[0])
        while any_obj > 0:
            if any_obj % 10 > 0:
                digit_arts.append(digits[any_obj % 10].replace('X', fruits[fruitIndex % len(fruits)]))
            any_obj //= 10
            fruitIndex += 1

        random.shuffle(digit_arts)
        for digit_art in digit_arts:
            result = _addTo(result, digit_art)
        result = _addTo(az.replace('X', the_type), result)
    elif isinstance(any_obj, str):
        the_type = '📝'
        result = pyfiglet.figlet_format(any_obj, font='script', width=sys.maxsize)
        result = _addTo(az.replace('X', the_type), result)
    elif isinstance(any_obj, list):
        result = '📜' + serialize(dict(enumerate(any_obj)))[1:]

    elif isinstance(any_obj, dict):
        # type is dictionary:
        the_type = '📖'
        result = '\n'
        items = list(any_obj.items())
        random.shuffle(items)
        keys = [serialize(key) for key, value in items]
        values = [serialize(value) for key, value in items]

        width = max(len(k.splitlines()[-1]) for k in keys + values if len(k.splitlines()) == 7)
        prefix = "╔" + "═" * width + "╦" + "═" * width +"╗\n"
        infix = "╠" + "─" * width + "┼" + "─" * width +"╣\n"
        frame = "║\n" * 7
        frame_sep = "│\n" * 7
        suffix = "╚" + "═" * width + "╩" + "═" * width +"╝\n"

        result = prefix
        after_result = ""
        for i in range(len(items)):
            if i > 0:
                result += infix

            if len(keys[i].splitlines()) == 7:
                subres = _addTo(frame, keys[i])
            else:
                subres = az.replace('X', keys[i][0])
                after_result += keys[i] + "\n"
            subres = _addTo(subres, (' ' * (width - len(subres.splitlines()[0])) + '\n') * 7)
            subres = _addTo(subres, frame_sep)

            if len(values[i].splitlines()) == 7:
                subres = _addTo(subres, values[i])
            else:
                subres = _addTo(subres, az.replace('X', values[i][0]))
                after_result += values[i] + "\n"
            subres = _addTo(subres, (' ' * (width * 2 - len(subres.splitlines()[0])) + '\n') * 7)
            subres = _addTo(subres, frame)
            result += subres + '\n'

        result += suffix
        result += after_result

        result = _addTo(az.replace('X', the_type), result)
    else:
        result = ""
    return result

def deserialize(ascii_art):
    if not ascii_art:
        return None
    elif ascii_art[0] == '🔢':
        value = 0
        for fruit in reversed(fruits):
            value *= 10
            value += ascii_art.count(fruit)
        return value
    elif ascii_art[0] == '📝':
        return find_original_text('\n'.join(line[2:] for line in ('  ' + ascii_art[1:]).splitlines()))
    elif ascii_art[0] == '📜':
        dictionary = deserialize('📖' + ascii_art[1:])
        result = []
        for key in sorted(map(int, dictionary.keys())):
           result.append(dictionary[key])

        return result

    elif ascii_art[0] == '📖':
        obj = {}

        subs = ascii_art.split('╝\n')
        ix = 1
        while ix < len(subs):
            if subs[ix].startswith('   '):
                subs[ix-1] += subs[ix] + '╝\n'
                del subs[ix]
            else:
                subs[ix] += '╝\n'
                ix += 1

        next_sub = 1
        for elements in subs[0].split('╠'):
            the_lines = elements.splitlines()[1:-1]
            key = '\n'.join((line[3:len(line.split('│')[0])] for line in the_lines))
            value = '\n'.join((line[len(line.split('│')[0])+1:-1] for line in the_lines))

            if key[0] == '📜' or key[0] == '📖':
                k = deserialize('\n'.join(line[2:] for line in subs[next_sub].splitlines()))
                next_sub += 1
            else:
                k = deserialize(key)
            if value[0] == '📜' or value[0] == '📖':
                v = deserialize('\n'.join(line[2:] for line in subs[next_sub].splitlines()))
                next_sub += 1
            else:
                v = deserialize(value)
            if isinstance(k, str):
                k = k.strip()
            if isinstance(v, str):
                v = v.strip()
            obj[k] = v

        return obj
    else:
        return None
