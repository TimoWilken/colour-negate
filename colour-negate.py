#! /bin/env python3

import sys, os, re
from enum import Enum


class Direction(Enum):
    both = 'both'
    light_to_dark = 'ltd'
    dark_to_light = 'dtl'


def should_negate_colour(grayscale, negate_mode):
    if direction == Direction.both:
        return True
    elif direction == Direction.dark_to_light:
        return grayscale < 0x7F
    elif direction == Direction.light_to_dark:
        return grayscale > 0x7F
    raise ValueError('negate_mode = {!r}, but must be member of enum Direction'
                     .format(negate_mode))


def negate_colour(colour, direction=Direction.both):
    colour = colour.strip()
    m = re.fullmatch('#([0-9a-fA-F]{2}){3}', colour)
    if m:
        grayscale = int(m.group(1), 16)
        if should_negate_colour(grayscale, direction):
            negated = '#' + 3 * hex(0xFF - grayscale).replace('0x', '')
            print('\tnegated %s to %s' % (colour, negated))
            return negated
        else:
            print('\tskipping ignored colour: %s' % colour)
    else:
        print('\tskipping non-colour "%s"' % colour)
    return colour


def process_file(contents, direction=DIR_BOTH):
    hash_replace = '<<HASH>>'
    match = True
    while match:
        match = re.search('#([0-9a-fA-F]{2}){3}', contents)
        if not match:
            break
        colour = match.group(0)
        negated = negate_colour(colour, direction).replace('#', hash_replace)
        contents = contents.replace(colour, negated)
    return contents.replace(hash_replace, '#')


def process_directory(dir_path):
    for name, dirs, files in os.walk(dir_path):
        print(name, dirs, files, sep='\n', end='\n\n')
        for fname in files:
            fname = os.path.join(name, fname)
            print('processing: %s' % fname)
            with open(fname, 'r') as read_file:
                contents = read_file.read()
            new_contents = process_file(contents, DIR_DARK_TO_LIGHT)
            with open(fname, 'w') as write_file:
                write_file.write(new_contents)


def main():
    process_subdirs = sys.argv[1:] if len(sys.argv) > 1 else ['actions']
    for subdir in process_subdirs:
        process_directory(subdir)


if __name__ == '__main__':
    main()

