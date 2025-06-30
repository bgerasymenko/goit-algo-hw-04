#!/usr/bin/env python3
import argparse
import random
import timeit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def run_timings(sizes, num_runs):
    results = {'n': [], 'insertion': [], 'merge': [], 'timsort': []}
    for n in sizes:
        arr = [random.random() for _ in range(n)]
        # Measure average time over num_runs
        t_ins = timeit.timeit(lambda: insertion_sort(arr), number=num_runs)
        t_merge = timeit.timeit(lambda: merge_sort(arr), number=num_runs)
        t_timsort = timeit.timeit(lambda: sorted(arr), number=num_runs)
        results['n'].append(n)
        results['insertion'].append(t_ins / num_runs)
        results['merge'].append(t_merge / num_runs)
        results['timsort'].append(t_timsort / num_runs)
    return pd.DataFrame(results)

def plot_results(df, output_path):
    plt.figure(figsize=(8, 5))
    plt.plot(df['n'], df['insertion'], label='Insertion Sort', marker='o')
    plt.plot(df['n'], df['merge'],     label='Merge Sort',     marker='s')
    plt.plot(df['n'], df['timsort'],   label='Timsort (built-in)', marker='^')
    plt.xlabel('Input size (n)')
    plt.ylabel('Time (seconds)')
    plt.title('Sorting Algorithm Performance Comparison')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Сompare Insertion Sort, Merge Sort, and Python's built-in Timsort"
    )
    parser.add_argument('--sizes',
                        default='100,500,1000,2000',
                        help="Comma-separated list of input sizes to test (default: 100,500,1000,2000)")
    parser.add_argument('--runs',
                        type=int,
                        default=5,
                        help="Number of runs per input size to average (default: 5)")
    parser.add_argument('--csv',
                        default='timings.csv',
                        help="Output CSV file for timing results (default: timings.csv)")
    parser.add_argument('--plot',
                        default='performance_plot.png',
                        help="Output PNG file for performance plot (default: performance_plot.png)")
    args = parser.parse_args()

    sizes = [int(s) for s in args.sizes.split(',')]
    df = run_timings(sizes, args.runs)

    # Save and display results
    df.to_csv(args.csv, index=False)
    print(f"Timing results saved to {args.csv}")
    print(df.to_string(index=False))

    plot_results(df, args.plot)

if __name__ == "__main__":
    main()
