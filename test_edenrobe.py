import pytest

import config
import scenarios
from classes import CLASSES
from helpers import make_driver

# Valid tests that use a product: run once with each product type.
PRODUCT_TESTS = {'TC03', 'TC05', 'TC07', 'TC09'}

CASES = []
for tc in sorted(scenarios.TESTS):
    if tc in CLASSES:
        for cls in CLASSES[tc]:
            CASES.append(pytest.param(tc, cls, 1, id='%s-%s' % (tc, cls[0])))
    elif tc in PRODUCT_TESTS:
        for run in range(1, len(config.PRODUCTS) + 1):
            CASES.append(pytest.param(tc, None, run, id='%s-%s' % (tc, config.PRODUCTS[run - 1]['type'])))
    else:
        CASES.append(pytest.param(tc, None, 1, id='%s-valid' % tc))


@pytest.mark.parametrize('tc_id,cls,run', CASES)
def test_case(tc_id, cls, run):
    d = make_driver()
    try:
        ok, note = scenarios.TESTS[tc_id](d, cls, run)
    finally:
        d.quit()
    assert ok, note
