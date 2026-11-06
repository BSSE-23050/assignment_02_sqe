import csv
import math
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

GOAL = 90.0  # 90% Target Reliability Threshold


def ibeta(a, b, x, steps=500):
  """Numerical approximation of the Regularized Incomplete Beta Function."""
  if x <= 0:
    return 0.0
  if x >= 1:
    return 1.0

  h = x / steps
  total = 0.0
  for i in range(steps + 1):
    t = i * h
    val = 0.0 if (t == 0 or t == 1) else (t ** (a - 1)) * ((1 - t) ** (b - 1))
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


def calculate_metrics():
  """Reads summary.csv or results.csv and computes test metrics."""
  test_ids = [f'TC{i:02d}' for i in range(1, 11)]
  data = []

  # Read directly from summary.csv if available
  try:
    with open('summary.csv', mode='r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      for r in reader:
        data.append((
            r['test'],
            int(r['runs']),
            int(r['passed']),
            int(r['failed']),
            float(r['pass_rate']) * 100,
            float(r['lower_bound_1sided']) * 100,
            r['decision'],
        ))
  except FileNotFoundError:
    # Fallback to direct calculation from results.csv
    results = {tc: [] for tc in test_ids}
    with open('results.csv', mode='r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      for r in reader:
        tc = r.get('test_id') or r.get('TestID')
        res = r.get('result') or r.get('Status')
        if tc in results and res:
          results[tc].append(res.strip().upper())

    for tc in test_ids:
      runs = results[tc]
      n = len(runs)
      s = runs.count('PASS')
      f = n - s
      rate = (s / n) * 100 if n > 0 else 0
      low = (
          (0.0 if s == 0 else beta_ppf(0.05, s, n - s + 1)) * 100
          if n > 0
          else 0
      )
      dec = 'ACCEPT' if low >= GOAL else 'REJECT'
      data.append((tc, n, s, f, round(rate, 1), round(low, 1), dec))

  return data


def generate_plots():
  data = calculate_metrics()

  tests = [d[0] for d in data]
  runs = [d[1] for d in data]
  passed = [d[2] for d in data]
  failed = [d[3] for d in data]
  rates = [d[4] for d in data]
  lows = [d[5] for d in data]

  x = np.arange(len(tests))

  # Set styling parameters
  plt.rcParams['font.family'] = 'sans-serif'
  plt.rcParams['font.size'] = 10

  # -------------------------------------------------------------
  # Graph 1: Test Execution Breakdown & Decision Status (Stacked Bar Chart)
  # -------------------------------------------------------------
  fig, ax1 = plt.subplots(figsize=(10, 6))
  width = 0.55

  p1 = ax1.bar(x, passed, width, label='Passed', color='#2b5c8f')
  p2 = ax1.bar(x, failed, width, bottom=passed, label='Failed', color='#d95f02')

  for i, (p, f_val, r, low) in enumerate(zip(passed, failed, runs, lows)):
    status = 'ACCEPT' if low >= GOAL else 'REJECT'
    color = '#1b9e77' if status == 'ACCEPT' else '#e7298a'
    ax1.text(
        i,
        r + 1.5,
        f'{p}/{r}\n({status})',
        ha='center',
        va='bottom',
        fontsize=8,
        fontweight='bold',
        color=color,
    )

  ax1.set_xlabel('Test Case', fontweight='bold', labelpad=10)
  ax1.set_ylabel('Execution Count (Runs)', fontweight='bold', labelpad=10)
  ax1.set_title(
      'Edenrobe QA: Test Execution Breakdown & Acceptance Status',
      fontweight='bold',
      fontsize=12,
      pad=15,
  )
  ax1.set_xticks(x)
  ax1.set_xticklabels(tests)
  ax1.set_ylim(0, max(runs) + 12)
  ax1.legend(loc='upper right', frameon=True)
  ax1.grid(axis='y', linestyle='--', alpha=0.5)

  plt.tight_layout()
  chart1_path = 'test_execution_breakdown.png'
  plt.savefig(chart1_path, dpi=300)
  plt.close()
  print(f'Saved: {chart1_path}')

  # -------------------------------------------------------------
  # Graph 2: Statistical Reliability Assessment (Line & Lower Bound Plot)
  # -------------------------------------------------------------
  fig, ax2 = plt.subplots(figsize=(10, 6))

  ax2.plot(
      x,
      rates,
      marker='o',
      color='#2b5c8f',
      linewidth=2,
      label='Observed Pass Rate (%)',
  )
  ax2.plot(
      x,
      lows,
      marker='s',
      color='#7570b3',
      linewidth=2,
      linestyle='-',
      label='1-Sided 95% Lower Bound (%)',
  )
  ax2.axhline(
      GOAL,
      color='#d95f02',
      linestyle='--',
      linewidth=2,
      label=f'Target Reliability Goal ({GOAL}%)',
  )

  for i, low in enumerate(lows):
    if low >= GOAL:
      ax2.scatter(x[i], low, color='#1b9e77', s=90, zorder=5)
    else:
      ax2.scatter(x[i], low, color='#e7298a', s=90, zorder=5)
      ax2.annotate(
          f'Fail ({low}%)',
          (x[i], low),
          textcoords='offset points',
          xytext=(0, -15),
          ha='center',
          fontsize=8,
          fontweight='bold',
          color='#e7298a',
      )

  ax2.set_xlabel('Test Case', fontweight='bold', labelpad=10)
  ax2.set_ylabel('Percentage (%)', fontweight='bold', labelpad=10)
  ax2.set_title(
      'Statistical Reliability Assessment (95% Clopper-Pearson vs 90% Target'
      ' Goal)',
      fontweight='bold',
      fontsize=12,
      pad=15,
  )
  ax2.set_xticks(x)
  ax2.set_xticklabels(tests)
  ax2.set_ylim(70, 105)
  ax2.legend(loc='lower right', frameon=True)
  ax2.grid(True, linestyle='--', alpha=0.5)

  plt.tight_layout()
  chart2_path = 'statistical_reliability_analysis.png'
  plt.savefig(chart2_path, dpi=300)
  plt.close()
  print(f'Saved: {chart2_path}')


if __name__ == '__main__':
  generate_plots()