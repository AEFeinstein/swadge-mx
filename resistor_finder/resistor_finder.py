#!/bin/python3

class resistance:
    def __init__(self, r: float, meta: str):
        self.r = r
        self.meta = meta

def parallel_val(r1: float, r2: float) -> float:
    return 1 / ((1 / r1) + (1 / r2))

def series_val(r1: float, r2: float) -> float:
    return r1 + r2

def calc_ilim(r: float) -> float:
    k = (1610 + 1525) / 2
    return k / r

def calc_iset(r: float) -> float:
    return 890 / r

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

##############################################################################

used_vals: list[float] = [220, 2200, 10000, 120, 20000, 33, 5100, 12000, 100, 33000]

allVals.clear()

for r1 in used_vals:
    allVals.append(resistance(r1, f'single %f' % (r1)))
    for r2 in used_vals:
        allVals.append(resistance(parallel_val(r1, r2), f'parallel %f, %f' % (r1, r2)))
        allVals.append(resistance(series_val(r1, r2), f'series %f, %f' % (r1, r2)))
        for r3 in used_vals:
            allVals.append(resistance(series_val(series_val(r1, r2), r3), f'series %f, %f, %f' % (r1, r2, r3)))
            allVals.append(resistance(parallel_val(parallel_val(r1, r2), r3), f'parallel %f, %f, %f' % (r1, r2, r3)))

            allVals.append(resistance(series_val(parallel_val(r1, r2), r3), f'series %f, parallel %f, %f' % (r3, r1, r2)))
            allVals.append(resistance(series_val(parallel_val(r2, r3), r1), f'series %f, parallel %f, %f' % (r1, r2, r3)))
            allVals.append(resistance(series_val(parallel_val(r1, r3), r2), f'series %f, parallel %f, %f' % (r2, r1, r3)))

            allVals.append(resistance(parallel_val(series_val(r1, r2), r3), f'parallel %f, series %f, %f' % (r3, r1, r2)))
            allVals.append(resistance(parallel_val(series_val(r2, r3), r1), f'parallel %f, series %f, %f' % (r1, r2, r3)))
            allVals.append(resistance(parallel_val(series_val(r1, r3), r2), f'parallel %f, series %f, %f' % (r2, r1, r3)))

allVals.sort(key=lambda x:x.r)
for r in allVals:
    print(str(r.r) + ' ' + r.meta)

smallestDiff = 1000000

for r in allVals:
    ilim = calc_ilim(r.r)
    diff = abs(0.5 - ilim)
    if(diff < smallestDiff):
        smallestDiff = diff
        bestRes = r
print(f'ILIM: %s -> %f : %f' % (bestRes.meta, bestRes.r, calc_ilim(bestRes.r)))

##############################################################################

smallestDiff = 1000000

for r in allVals:
    iset = calc_iset(r.r)
    diff = abs(0.5 - iset)
    if(diff < smallestDiff):
        smallestDiff = diff
        bestRes = r
print(f'ISET: %s -> %f : %f' % (bestRes.meta, bestRes.r, calc_iset(bestRes.r)))