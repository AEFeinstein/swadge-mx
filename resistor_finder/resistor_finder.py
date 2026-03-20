#!/bin/python3

class resistance:
    def __init__(self, r: float, meta: str):
        self.r = r
        self.meta = meta

def parallel_val(r1: float, r2: float) -> float:
    return 1 / ((1 / r1) + (1 / r2))

def series_val(r1: float, r2: float) -> float:
    return r1 + r2

e12_vals = [10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68, 82]

allVals: list[resistance] = []

for r1 in e12_vals:
    allVals.append(resistance(r1, f'single %f' % (r1)))
    for r2 in e12_vals:
        allVals.append(resistance(parallel_val(r1, r2), f'parallel %f, %f' % (r1, r2)))
        allVals.append(resistance(series_val(r1, r2), f'series %f, %f' % (r1, r2)))

smallestDiff = 1000000

for r1 in allVals:
    for r2 in allVals:
        v = 0.6 * (1 + r1.r / r2.r)
        diff = abs(3.3 - v)
        if 0 == diff:
            print(f'zero: %s %s' % (r1.meta, r2.meta))
        if diff < smallestDiff:
            smallestDiff = diff
            bestR1 = r1
            bestR2 = r2

print(bestR1.meta)
print(bestR2.meta)
print(0.6 * (1 + bestR1.r / bestR2.r))