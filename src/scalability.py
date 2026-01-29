import random
import time
import sys
import os

import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from matcher import gale_shapley
from verifier import check_validity, check_stability

def generate_random_prefs(n):
    hospital_prefs = {}
    student_prefs = {}
    for i in range(1, n + 1):
        prefs = list(range(1, n + 1))
        random.shuffle(prefs)
        hospital_prefs[i] = prefs
    for i in range(1, n + 1):
        prefs = list(range(1, n + 1))
        random.shuffle(prefs)
        student_prefs[i] = prefs
    return hospital_prefs, student_prefs

def measure_matcher(n, hospital_prefs, student_prefs):
    start = time.perf_counter()
    matching, _ = gale_shapley(n, hospital_prefs, student_prefs)
    end = time.perf_counter()
    return matching, end - start

def measure_verifier(n, matching, hospital_prefs, student_prefs):
    start = time.perf_counter()
    check_validity(n, matching)
    check_stability(n, matching, hospital_prefs, student_prefs)
    end = time.perf_counter()
    return end - start

def main():
    sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    matcher_times = []
    verifier_times = []

    print("n,matcher_time_ms,verifier_time_ms")
    for n in sizes:
        hospital_prefs, student_prefs = generate_random_prefs(n)

        matching, m_time = measure_matcher(n, hospital_prefs, student_prefs)
        v_time = measure_verifier(n, matching, hospital_prefs, student_prefs)

        matcher_times.append(m_time * 1000)
        verifier_times.append(v_time * 1000)
        print(f"{n},{m_time*1000:.4f},{v_time*1000:.4f}")


    plt.figure(figsize=(10, 6))
    plt.plot(sizes, matcher_times, 'b-o', label='Matcher')
    plt.plot(sizes, verifier_times, 'r-s', label='Verifier')
    plt.xlabel('n (number of hospitals/students)')
    plt.ylabel('Running Time (ms)')
    plt.title('Scalability: Running Time vs Problem Size')
    plt.legend()
    plt.grid(True)
    plt.xscale('log', base=2)
    plt.savefig('data/scalability_graph.png', dpi=150)
    print("\nGraph saved to data/scalability_graph.png")

if __name__ == "__main__":
    main()
