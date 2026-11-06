import csv
import math

GOAL = 0.90
UC = {
    'TC01': 'UC1 Registration',
    'TC02': 'UC1 Registration',
    'TC03': 'UC2 Order (logged in)',
    'TC04': 'UC2 Order (logged in)',
    'TC05': 'UC3 Order (guest)',
    'TC06': 'UC3 Order (guest)',
    'TC07': 'UC4 Shopping cart',
    'TC08': 'UC4 Shopping cart',
    'TC09': 'UC5 Continue shopping',
    'TC10': 'UC5 Continue shopping',
}
KIND = {
    t: ('valid' if i % 2 == 0 else 'invalid')
    for i, t in enumerate(sorted(UC))
}


def ibeta(a, b, x, steps=500):
  """Numerical approximation of the Regularized Incomplete Beta Function."""
  if x <= 0:
    return 0.0
  if x >= 1:
    return 1.0

  # Simpson's rule integration over [0, x] for t^(a-1) * (1-t)^(b-1)
  h = x / steps
  total = 0.0
  for i in range(steps + 1):
    t = i * h
    if t == 0 or t == 1:
      val = 0.0
    else:
      val = (t ** (a - 1)) * ((1 - t) ** (b - 1))

    if i == 0 or i == steps:
      total += val
    elif i % 2 == 1:
      total += 4 * val
    else:
      total += 2 * val

  integral = total * (h / 3.0)
  beta_const = math.gamma(a) * math.gamma(b) / math.gamma(a + b)
  return min(1.0, max(0.0, integral / beta_const))


def beta_ppf(target_p, a, b):
  """Bisection solver for Beta Distribution Quantile Function."""
  low, high = 0.0, 1.0
  for _ in range(30):
    mid = (low + high) / 2.0
    if ibeta(a, b, mid) < target_p:
      low = mid
    else:
      high = mid
  return (low + high) / 2.0


def lower(s, n, alpha):
  return 0.0 if s == 0 else beta_ppf(alpha, s, n - s + 1)


def upper(s, n, alpha):
  return 1.0 if s == n else beta_ppf(1 - alpha, s + 1, n - s)


def main():
  # 1. Read results.csv
  results_by_tc = {tc: [] for tc in sorted(UC)}
  try:
    with open('results.csv', mode='r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      for row in reader:
        tc = row.get('test_id') or row.get('TestID')
        res = row.get('result') or row.get('Status')
        if tc in results_by_tc and res:
          results_by_tc[tc].append(res.strip().upper())
  except FileNotFoundError:
    print('Error: results.csv not found.')
    return

  summary_rows = []
  print('=' * 85)
  print(
      f"{'Test':<6} | {'Use Case':<22} | {'Kind':<7} | {'Runs':<4} |"
      f" {'Pass':<4} | {'Fail':<4} | {'Rate':<6} | {'1s-Low':<6} | {'Decision'}"
  )
  print('=' * 85)

  for tc in sorted(UC):
    runs = results_by_tc[tc]
    n = len(runs)
    if n == 0:
      continue
    s = runs.count('PASS')
    failed = n - s
    pass_rate = s / n
    lo1 = lower(s, n, 0.05)
    ci95_low = lower(s, n, 0.025)
    ci95_high = upper(s, n, 0.025)
    decision = 'ACCEPT' if lo1 >= GOAL else 'REJECT'

    row = {
        'test': tc,
        'use_case': UC[tc],
        'kind': KIND[tc],
        'runs': n,
        'passed': s,
        'failed': failed,
        'pass_rate': round(pass_rate, 4),
        'ci95_low': round(ci95_low, 4),
        'ci95_high': round(ci95_high, 4),
        'lower_bound_1sided': round(lo1, 4),
        'decision': decision,
    }
    summary_rows.append(row)

    print(
        f"{tc:<6} | {UC[tc]:<22} | {KIND[tc]:<7} | {n:<4} | {s:<4} |"
        f" {failed:<4} | {pass_rate*100:>5.1f}% | {lo1*100:>5.1f}% |"
        f' {decision}'
    )

  # 2. Write summary.csv
  fieldnames = [
      'test',
      'use_case',
      'kind',
      'runs',
      'passed',
      'failed',
      'pass_rate',
      'ci95_low',
      'ci95_high',
      'lower_bound_1sided',
      'decision',
  ]
  with open('summary.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(summary_rows)

  print('=' * 85)
  print('\nSaved summary statistics to summary.csv.')


if __name__ == '__main__':
  main()