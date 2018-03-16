from __future__ import division
import sys
import argparse
import wand.image

IS_PY3 = sys.version_info.major >= 3

def get_grays(image, width, height):
    #Convert to gray-scale
    if isinstance(image, (tuple, list)):
        if len(image) != width * height:
            raise ValueError('image sequence length ({}) not equal to width*height ({})'.format(
                    len(image), width * height))
        return image

    with image.clone() as image1:
        image1.type = 'grayscale'
        image1.resize(width, height)
        blob = image1.make_blob(format='RGB')
        return list(blob[::3])

def dhash_row_col(image, size=8):
    #Calculate row and column difference hash for given image and return
    #hashes as (row_hash, col_hash) where each value is a size*size bit
    #integer.
    width = size + 1
    grays = get_grays(image, width, width)

    row_hash = 0
    col_hash = 0
    for y in range(size):
        for x in range(size):
            offset = y * width + x
            row_bit = grays[offset] < grays[offset + 1]
            row_hash = row_hash << 1 | row_bit

            col_bit = grays[offset] < grays[offset + width]
            col_hash = col_hash << 1 | col_bit

    return (row_hash, col_hash)


def dhash_int(image, size=8):
    #Calculate row and column difference hash for given image and return
    #hashes combined as a single 2*size*size bit integer (row_hash in most
    #significant bits, col_hash in least).
    row_hash, col_hash = dhash_row_col(image, size=size)
    return row_hash << (size * size) | col_hash


def get_num_bits_different(hash1, hash2):
    #Calculate number of bits different between two hashes.
    return bin(hash1 ^ hash2).count('1')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=int, default=8)
    parser.add_argument('filename',nargs='*')
    args = parser.parse_args()

    def load_image(filename):
        if wand is not None:
            return wand.image.Image(filename=filename)
        else:
            sys.stderr.write('You must have Wand installed to use the dhash command\n')
            sys.exit(1)

    if len(args.filename) == 1:
        image = load_image(args.filename[0])
        row_hash, col_hash = dhash_row_col(image, size=args.size)
        print(row_hash, col_hash)

    elif len(args.filename) == 2:
        image1 = load_image(args.filename[0])
        image2 = load_image(args.filename[1])
        hash1 = dhash_int(image1, size=args.size)
        hash2 = dhash_int(image2, size=args.size)
        num_bits_different = get_num_bits_different(hash1, hash2)
        print('{} {} out of {} ({:.1f}%)'.format(
                num_bits_different,
                'bit differs' if num_bits_different == 1 else 'bits differ',
                args.size * args.size * 2,
                100 * num_bits_different / (args.size * args.size * 2)))
