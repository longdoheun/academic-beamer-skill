#!/usr/bin/env python3
"""Pure arithmetic helpers. Dimensions are mm; font values share a point unit."""
import argparse
import json
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Grid:
    width: float = 160
    left: float = 7
    right: float = 7
    columns: int = 6
    gutter: float = 6

    def __post_init__(self):
        if type(self.columns) is not int or self.columns < 1:
            raise ValueError('columns must be a positive integer')
        if not all(isfinite(x) for x in (self.width, self.left, self.right, self.gutter)):
            raise ValueError('dimensions must be finite')
        if min(self.left, self.right, self.gutter) < 0 or self.track <= 0:
            raise ValueError('nonnegative spacing and positive track width required')

    @property
    def usable(self):
        return self.width - self.left - self.right

    @property
    def track(self):
        return (self.usable - (self.columns - 1) * self.gutter) / self.columns

    def span(self, count):
        if type(count) is not int or not 1 <= count <= self.columns:
            raise ValueError('span outside valid integer range')
        return count * self.track + (count - 1) * self.gutter

    def row(self, counts):
        if not counts or sum(counts) != self.columns:
            raise ValueError('row spans must sum to columns')
        widths = [self.span(k) for k in counts]
        return {'widths_mm': widths, 'total_mm': sum(widths) + (len(counts) - 1) * self.gutter}


def figure_fit(slot_width, slot_height, native_width, native_height, native_font, min_font):
    values = (slot_width, slot_height, native_width, native_height, native_font, min_font)
    if not all(isfinite(x) and x > 0 for x in values):
        raise ValueError('complete positive figure dimensions and font sizes required')
    scale = min(slot_width / native_width, slot_height / native_height)
    return {'scale': scale, 'final_font': scale * native_font,
            'readable': scale * native_font >= min_font}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--width', type=float, default=160)
    p.add_argument('--left', type=float, default=7)
    p.add_argument('--right', type=float, default=7)
    p.add_argument('--columns', type=int, default=6)
    p.add_argument('--gutter', type=float, default=6)
    p.add_argument('--spans', type=int, nargs='+', default=[4, 2])
    a = p.parse_args()
    g = Grid(a.width, a.left, a.right, a.columns, a.gutter)
    print(json.dumps({'usable_mm': g.usable, 'track_mm': g.track, **g.row(a.spans)}, indent=2))


if __name__ == '__main__':
    main()
