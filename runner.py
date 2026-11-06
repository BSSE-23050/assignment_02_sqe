import csv
import os
import random
import sys
import time
from datetime import datetime

import config
import scenarios
from classes import CLASSES
from helpers import make_driver

FIELDS = ['test_id', 'run', 'class_id', 'product_type', 'result', 'seconds', 'note', 'timestamp']


def done_runs(tc):
    if not os.path.exists('results.csv'):
        return 0
    with open('results.csv') as f:
        return sum(1 for r in csv.DictReader(f) if r['test_id'] == tc)


tc, total = sys.argv[1].upper(), int(sys.argv[2])
os.makedirs('screens', exist_ok=True)
n = done_runs(tc)
while n < total:
    n += 1
    cls, cid = None, 'valid'
    if tc in CLASSES:                          # data-driven invalid test: next class in turn
        cls = CLASSES[tc][(n - 1) % len(CLASSES[tc])]
        cid = cls[0]
    scenarios.STATE['types'] = []
    d = make_driver()
    t0 = time.time()
    try:
        ok, note = scenarios.TESTS[tc](d, cls, n)
    except Exception as e:
        ok, note = False, 'EXC %s %s' % (type(e).__name__, str(e)[:80].replace('\n', ' '))
    if not ok:
        d.save_screenshot('screens/%s_%02d_%s.png' % (tc, n, cid))
    d.quit()
    new_file = not os.path.exists('results.csv')
    with open('results.csv', 'a', newline='') as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(FIELDS)
        w.writerow([tc, n, cid, '+'.join(scenarios.STATE['types']) or '-',
                    'PASS' if ok else 'FAIL', round(time.time() - t0, 1), note,
                    datetime.now().isoformat(timespec='seconds')])
    print(tc, n, cid, 'PASS' if ok else 'FAIL', note)
    time.sleep(random.uniform(*config.PAUSE))
