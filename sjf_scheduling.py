"""
CS11335 Operating Systems – Course Project
Princess Sumaya University for Technology
King Hussein School of Computing Sciences

Algorithm : Shortest-Job-First (SJF) – Non-Preemptive
Language  : Python 3

Description:
    SJF selects the process with the smallest burst time from all
    processes that have already arrived. Once a process starts, it
    runs to completion (non-preemptive). If the CPU is idle and no
    process has arrived yet, it waits until the next arrival.

Metrics computed (as required by the project):
    - Turnaround Time (TAT) = Finish Time - Arrival Time
    - Waiting Time (WT)     = Turnaround Time - Burst Time
    - Average TAT and Average WT across all processes
"""


# ──────────────────────────────────────────────────────────────────────────────
#  Core Algorithm
# ──────────────────────────────────────────────────────────────────────────────

def sjf_non_preemptive(processes):
    """
    Run SJF Non-Preemptive scheduling on a list of processes.

    Parameters
    ----------
    processes : list of dict
        Each dict must contain:
            'pid'      (str)  – process identifier, e.g. 'P1'
            'arrival'  (int)  – arrival time
            'burst'    (int)  – CPU burst time
            'priority' (int)  – kept for group compatibility (unused by SJF)

    Returns
    -------
    results             : list of dict  – per-process computed metrics
    avg_waiting_time    : float
    avg_turnaround_time : float
    """
    n = len(processes)
    procs = [p.copy() for p in processes]   # never mutate the caller's list
    done = [False] * n
    completed = []
    current_time = 0

    for _ in range(n):
        # Collect processes that have arrived and are not yet finished
        available = [
            procs[i] for i in range(n)
            if not done[i] and procs[i]['arrival'] <= current_time
        ]

        # If nothing is ready, jump forward to the next arrival (CPU idle)
        if not available:
            current_time = min(
                procs[i]['arrival'] for i in range(n) if not done[i]
            )
            available = [
                procs[i] for i in range(n)
                if not done[i] and procs[i]['arrival'] <= current_time
            ]

        # Pick shortest burst; break ties by arrival time then PID
        selected = min(
            available,
            key=lambda p: (p['burst'], p['arrival'], p['pid'])
        )

        start_time      = current_time
        finish_time     = start_time + selected['burst']
        turnaround_time = finish_time - selected['arrival']
        waiting_time    = turnaround_time - selected['burst']
        current_time    = finish_time

        idx = next(i for i in range(n) if procs[i]['pid'] == selected['pid'])
        done[idx] = True

        completed.append({
            'pid'            : selected['pid'],
            'arrival'        : selected['arrival'],
            'burst'          : selected['burst'],
            'start'          : start_time,
            'finish'         : finish_time,
            'turnaround_time': turnaround_time,
            'waiting_time'   : waiting_time,
        })

    avg_wt  = sum(p['waiting_time']    for p in completed) / n
    avg_tat = sum(p['turnaround_time'] for p in completed) / n

    return completed, avg_wt, avg_tat


# ──────────────────────────────────────────────────────────────────────────────
#  Display
# ──────────────────────────────────────────────────────────────────────────────

def print_results(results, avg_wt, avg_tat, title="SJF (Non-Preemptive)"):
    """Print a formatted results table to the console."""
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


# ──────────────────────────────────────────────────────────────────────────────
#  Shared process set  ← YOUR GROUP EDITS THIS ONE LIST
# ──────────────────────────────────────────────────────────────────────────────
#
#  Every teammate's script should use the SAME process list so that the
#  group comparison of Avg TAT and Avg WT is fair and consistent.
#
#  Fields:
#    pid      – process name
#    arrival  – arrival time (time units)
#    burst    – CPU burst time (time units)
#    priority – used by Priority Scheduling teammates; SJF ignores it

SHARED_PROCESSES = [
    {'pid': 'P1', 'arrival': 0, 'burst': 6, 'priority': 3},
    {'pid': 'P2', 'arrival': 1, 'burst': 8, 'priority': 2},
    {'pid': 'P3', 'arrival': 2, 'burst': 7, 'priority': 4},
    {'pid': 'P4', 'arrival': 3, 'burst': 3, 'priority': 1},
    {'pid': 'P5', 'arrival': 4, 'burst': 4, 'priority': 5},
]


# ──────────────────────────────────────────────────────────────────────────────
#  Test suite  (validates correctness against hand-computed expected values)
# ──────────────────────────────────────────────────────────────────────────────

def run_test(name, processes, expected_avg_wt=None, expected_avg_tat=None):
    results, avg_wt, avg_tat = sjf_non_preemptive(processes)
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

    # Test 1: All arrive at time 0
    # SJF order: P3(2) -> P4(4) -> P1(6) -> P2(8)
    # WT : 0, 2, 6, 12   -> Avg WT  = 5.00
    # TAT: 2, 6, 12, 20  -> Avg TAT = 10.00
    all_passed &= run_test(
        "All arrive at t=0 — pure burst sorting",
        [
            {'pid': 'P1', 'arrival': 0, 'burst': 6, 'priority': 2},
            {'pid': 'P2', 'arrival': 0, 'burst': 8, 'priority': 1},
            {'pid': 'P3', 'arrival': 0, 'burst': 2, 'priority': 3},
            {'pid': 'P4', 'arrival': 0, 'burst': 4, 'priority': 4},
        ],
        expected_avg_wt=5.00,
        expected_avg_tat=10.00,
    )

    # Test 2: Staggered arrivals
    # P1 only process at t=0. At t=6: P2(8),P3(7),P4(3) available.
    # Order: P1 -> P4 -> P3 -> P2
    # WT : 0, 3, 7, 15   -> Avg WT  = 6.25
    # TAT: 6, 6, 14, 23  -> Avg TAT = 12.25
    all_passed &= run_test(
        "Staggered arrivals — decision point at t=6",
        [
            {'pid': 'P1', 'arrival': 0, 'burst': 6, 'priority': 3},
            {'pid': 'P2', 'arrival': 1, 'burst': 8, 'priority': 2},
            {'pid': 'P3', 'arrival': 2, 'burst': 7, 'priority': 4},
            {'pid': 'P4', 'arrival': 3, 'burst': 3, 'priority': 1},
        ],
        expected_avg_wt=6.25,
        expected_avg_tat=12.25,
    )

    # Test 3: CPU idle gap
    # P1 ends at t=4; P2 arrives at t=7 -> CPU idles 3 units.
    # Order: P1(0->4) -> idle(4->7) -> P2(7->15) -> P3(15->20)
    # WT : 0, 0, 5       -> Avg WT  = 1.67
    # TAT: 4, 8, 10      -> Avg TAT = 7.33
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

    # Test 4: Tie-breaking on equal burst time
    # P3(burst=4) runs first. P1 and P2 tie on burst=5 -> broken by PID.
    # Order: P3(0->4) -> P1(4->9) -> P2(9->14)
    # WT : 0, 4, 9       -> Avg WT  = 4.33
    # TAT: 4, 9, 14      -> Avg TAT = 9.00
    all_passed &= run_test(
        "Tie-breaking — equal burst, broken by PID",
        [
            {'pid': 'P1', 'arrival': 0, 'burst': 5, 'priority': 2},
            {'pid': 'P2', 'arrival': 0, 'burst': 5, 'priority': 1},
            {'pid': 'P3', 'arrival': 0, 'burst': 4, 'priority': 3},
        ],
        expected_avg_wt=4.33,
        expected_avg_tat=9.00,
    )

    # Test 5: Single process edge case
    # No contention. WT = 0, TAT = burst.
    all_passed &= run_test(
        "Single process — edge case",
        [
            {'pid': 'P1', 'arrival': 3, 'burst': 9, 'priority': 1},
        ],
        expected_avg_wt=0.00,
        expected_avg_tat=9.00,
    )

    # Test 6: Large set — 6 processes
    # P1 runs 0->10. At t=10 all others arrived.
    # SJF order from t=10: P2(1)->P6(2)->P4(3)->P3(5)->P5(7)
    # TAT: 10, 9,  5, 12, 17, 22  -> Avg TAT = 12.50
    # WT :  0, 8,  3,  9, 12, 15  -> Avg WT  =  7.83
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
        expected_avg_wt=7.83,
        expected_avg_tat=12.50,
    )

    print("\n" + "=" * 56)
    print(f"  TEST SUITE: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    print("=" * 56 + "\n")


# ──────────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 1) Run on the shared group process set (required for project comparison)
    print("\n" + "#" * 56)
    print("  SHARED GROUP PROCESS SET — SJF Non-Preemptive")
    print("#" * 56)
    results, avg_wt, avg_tat = sjf_non_preemptive(SHARED_PROCESSES)
    print_results(results, avg_wt, avg_tat,
                  title="SJF (Non-Preemptive) — Group Comparison")

    # 2) Run the full test suite
    print("\n" + "#" * 56)
    print("  RUNNING TEST SUITE")
    print("#" * 56)
    run_all_tests()
