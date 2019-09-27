#!/usr/bin/env python3

'''Negate HTML colours in files.

This is useful for converting light SVG icon themes to dark ones or vice versa.

Currently only handles grayscale colours.
'''

import sys
import os
import re
from enum import Enum


class Direction(Enum):
    '''Which colours to invert.'''
    both = 'both'          # invert all colours
    light_to_dark = 'ltd'  # invert light colours only
    dark_to_light = 'dtl'  # invert dark colours only


def should_negate_colour(grayscale, negate_mode):
    '''Whether a grayscale colour should be negated according to negate_mode.'''
    if negate_mode == Direction.both:
        return True
    if negate_mode == Direction.dark_to_light:
        return grayscale < 0x7F
    if negate_mode == Direction.light_to_dark:
        return grayscale > 0x7F
    raise ValueError('negate_mode = {!r}, but must be member of enum Direction'
                     .format(negate_mode))


def negate_colour(colour, direction=Direction.both):
    '''Return colour negated or not, according to direction.'''
    colour = colour.strip()
    match = re.fullmatch('#([0-9a-fA-F]{2}){3}', colour)
    if match:
        grayscale = int(match.group(1), 16)
        if should_negate_colour(grayscale, direction):
            negated = '#' + 3 * hex(0xFF - grayscale).replace('0x', '')
            print('\tnegated %s to %s' % (colour, negated))
            return negated
        print('\tskipping ignored colour: %s' % colour)
    else:
        print('\tskipping non-colour "%s"' % colour)
    return colour


def process_file(contents, direction=Direction.both):
    '''Replace colours in contents with their negations (in given direction).'''
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


def process_directory(dir_path, direction=Direction.both):
    '''Invert colours in all files in the given directory.'''
    for name, dirs, files in os.walk(dir_path):
        print(name, dirs, files, sep='\n', end='\n\n')
        for fname in files:
            fname = os.path.join(name, fname)
            print('processing: %s' % fname)
            with open(fname, 'r') as read_file:
                contents = read_file.read()
            new_contents = process_file(contents, direction)
            with open(fname, 'w') as write_file:
                write_file.write(new_contents)


def main():
    '''Main entry point.'''
    process_subdirs = sys.argv[1:] if len(sys.argv) > 1 else ['actions']
    for subdir in process_subdirs:
        process_directory(subdir, Direction.dark_to_light)


if __name__ == '__main__':
    main()
