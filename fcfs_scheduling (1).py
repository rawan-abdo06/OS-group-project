# CS11335 Operating Systems
# Princess Sumaya University for Technology
# Algorithm: First-Come First-Served (FCFS) - Non-Preemptive


def fcfs(processes):
    # sort by arrival time, if two processes arrive at the same time use pid to decide
    procs = sorted(processes, key=lambda p: (p['arrival'], p['pid']))
    n = len(procs)

    completed = []
    current_time = 0

    for proc in procs:
        # cpu is idle, jump to when this process arrives
        if current_time < proc['arrival']:
            current_time = proc['arrival']

        start_time = current_time
        finish_time = start_time + proc['burst']
        tat = finish_time - proc['arrival']
        wt = tat - proc['burst']
        current_time = finish_time

        completed.append({
            'pid': proc['pid'],
            'arrival': proc['arrival'],
            'burst': proc['burst'],
            'start': start_time,
            'finish': finish_time,
            'turnaround_time': tat,
            'waiting_time': wt,
        })

    avg_wt = sum(p['waiting_time'] for p in completed) / n
    avg_tat = sum(p['turnaround_time'] for p in completed) / n

    return completed, avg_wt, avg_tat


def print_results(results, avg_wt, avg_tat, title="FCFS (Non-Preemptive)"):
    W = 56
    print("\n" + "=" * W)
    print(f"  {title}")
    print("=" * W)
    print(f"  {'PID':<5} {'Arrival':>7} {'Burst':>6} {'Start':>6} "
          f"{'Finish':>7} {'TAT':>5} {'WT':>5}")
    print("-" * W)
    for p in results:
        print(f"  {p['pid']:<5} {p['arrival']:>7} {p['burst']:>6} "
              f"{p['start']:>6} {p['finish']:>7} "
              f"{p['turnaround_time']:>5} {p['waiting_time']:>5}")
    print("-" * W)
    print(f"  Average Turnaround Time (Avg TAT) : {avg_tat:.2f}")
    print(f"  Average Waiting Time    (Avg WT)  : {avg_wt:.2f}")
    print("=" * W + "\n")


# all teammates use this same list so we can compare results fairly
SHARED_PROCESSES = [
    {'pid': 'P1', 'arrival': 0, 'burst': 6, 'priority': 3},
    {'pid': 'P2', 'arrival': 1, 'burst': 8, 'priority': 2},
    {'pid': 'P3', 'arrival': 2, 'burst': 7, 'priority': 4},
    {'pid': 'P4', 'arrival': 3, 'burst': 3, 'priority': 1},
    {'pid': 'P5', 'arrival': 4, 'burst': 4, 'priority': 5},
]


def run_test(name, processes, expected_avg_wt=None, expected_avg_tat=None):
    results, avg_wt, avg_tat = fcfs(processes)
    print(f"\n  TEST: {name}")
    print_results(results, avg_wt, avg_tat)

    passed = True
    if expected_avg_wt is not None:
        ok = abs(avg_wt - expected_avg_wt) < 0.01
        print(f"  Avg WT  -> expected {expected_avg_wt:.2f}, got {avg_wt:.2f}  [{'PASS' if ok else 'FAIL'}]")
        passed &= ok
    if expected_avg_tat is not None:
        ok = abs(avg_tat - expected_avg_tat) < 0.01
        print(f"  Avg TAT -> expected {expected_avg_tat:.2f}, got {avg_tat:.2f}  [{'PASS' if ok else 'FAIL'}]")
        passed &= ok
    return passed


def run_all_tests():
    all_passed = True

    all_passed &= run_test(
        "All arrive at t=0 — order by PID",
        [
            {'pid': 'P1', 'arrival': 0, 'burst': 6, 'priority': 2},
            {'pid': 'P2', 'arrival': 0, 'burst': 8, 'priority': 1},
            {'pid': 'P3', 'arrival': 0, 'burst': 2, 'priority': 3},
            {'pid': 'P4', 'arrival': 0, 'burst': 4, 'priority': 4},
        ],
        expected_avg_wt=9.00,
        expected_avg_tat=14.00,
    )

    all_passed &= run_test(
        "Staggered arrivals",
        [
            {'pid': 'P1', 'arrival': 0, 'burst': 6, 'priority': 3},
            {'pid': 'P2', 'arrival': 1, 'burst': 8, 'priority': 2},
            {'pid': 'P3', 'arrival': 2, 'burst': 7, 'priority': 4},
            {'pid': 'P4', 'arrival': 3, 'burst': 3, 'priority': 1},
        ],
        expected_avg_wt=8.75,
        expected_avg_tat=14.75,
    )

    # P1 finishes at t=4 but P2 doesnt show up until t=7, so cpu waits
    all_passed &= run_test(
        "CPU idle gap — no process ready at t=4",
        [
            {'pid': 'P1', 'arrival': 0,  'burst': 4, 'priority': 1},
            {'pid': 'P2', 'arrival': 7,  'burst': 8, 'priority': 2},
            {'pid': 'P3', 'arrival': 10, 'burst': 5, 'priority': 3},
        ],
        expected_avg_wt=1.67,
        expected_avg_tat=7.33,
    )

    all_passed &= run_test(
        "Tie on arrival — broken by PID",
        [
            {'pid': 'P1', 'arrival': 0, 'burst': 5, 'priority': 2},
            {'pid': 'P2', 'arrival': 0, 'burst': 5, 'priority': 1},
            {'pid': 'P3', 'arrival': 0, 'burst': 4, 'priority': 3},
        ],
        expected_avg_wt=5.00,
        expected_avg_tat=9.67,
    )

    all_passed &= run_test(
        "Single process — edge case",
        [
            {'pid': 'P1', 'arrival': 3, 'burst': 9, 'priority': 1},
        ],
        expected_avg_wt=0.00,
        expected_avg_tat=9.00,
    )

    all_passed &= run_test(
        "Large set — 6 processes with varied arrivals",
        [
            {'pid': 'P1', 'arrival': 0, 'burst': 10, 'priority': 3},
            {'pid': 'P2', 'arrival': 2, 'burst': 1,  'priority': 5},
            {'pid': 'P3', 'arrival': 4, 'burst': 5,  'priority': 2},
            {'pid': 'P4', 'arrival': 4, 'burst': 3,  'priority': 1},
            {'pid': 'P5', 'arrival': 6, 'burst': 7,  'priority': 4},
            {'pid': 'P6', 'arrival': 8, 'burst': 2,  'priority': 6},
        ],
        expected_avg_wt=9.67,
        expected_avg_tat=14.33,
    )

    print("\n" + "=" * 56)
    print(f"  TEST SUITE: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    print("=" * 56 + "\n")


if __name__ == "__main__":
    print("\n" + "#" * 56)
    print("  SHARED GROUP PROCESS SET — FCFS Non-Preemptive")
    print("#" * 56)
    results, avg_wt, avg_tat = fcfs(SHARED_PROCESSES)
    print_results(results, avg_wt, avg_tat,
                  title="FCFS (Non-Preemptive) — Group Comparison")

    print("\n" + "#" * 56)
    print("  RUNNING TEST SUITE")
    print("#" * 56)
    run_all_tests()
