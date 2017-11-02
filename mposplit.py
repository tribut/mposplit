#!/usr/bin/env python3

import argparse
from pathlib import Path
from PIL import Image


parser = argparse.ArgumentParser(
    description='Split MPO files foo.jpg into foo-0.jpg, foo-1.jpg, ...')
parser.add_argument(
    'file',
    help='MPO file(s) to be split',
    nargs='+')
args = parser.parse_args()

for file in args.file:
    print('== Processing {} =='.format(file))
    path = Path(file).resolve()

    try:
        image = Image.open(path)
    except IOError as e:
        print('Could not read image: {}'.format(e))
        continue

    if (image.format != 'MPO'):
        print('Format ' + image.format +
              ' not recognized as MPO, this script may not work')

    try:
        position = 0
        while True:
            image.seek(position)
            filename = '{}-{}{}'.format(path.stem, position, path.suffix)
            fullname = path.parent.joinpath(filename)

            if fullname.exists():
                print('{} already exists - skipping.'.format(filename))
            else:
                print('Extracting image to {}'.format(filename))

            try:
                image.save(fullname)
            except IOError as e:
                print('  Could not save: {}'.format(e))

            position = image.tell() + 1
    except EOFError:
        pass  # All images processed
