"""
CS11335 Operating Systems – Course Project
Princess Sumaya University for Technology
King Hussein School of Computing Sciences

Algorithm : First-Come First-Served (FCFS) – Non-Preemptive
Language  : Python 3

Description:
    FCFS runs processes in the order they arrive. The process that
    arrives first gets the CPU first and runs until it finishes.
    If two processes arrive at the same time, the one with the
    smaller PID goes first. If the CPU finishes before the next
    process arrives, it sits idle until that process shows up.

Metrics computed (as required by the project):
    - Turnaround Time (TAT) = Finish Time - Arrival Time
    - Waiting Time (WT)     = Turnaround Time - Burst Time
    - Average TAT and Average WT across all processes
"""


# ──────────────────────────────────────────────────────────────────────────────
#  Core Algorithm
# ──────────────────────────────────────────────────────────────────────────────

def fcfs(processes):
    """
    Run FCFS Non-Preemptive scheduling on a list of processes.

    Parameters
    ----------
    processes : list of dict
        Each dict must contain:
            'pid'      (str)  – process identifier, e.g. 'P1'
            'arrival'  (int)  – arrival time
            'burst'    (int)  – CPU burst time
            'priority' (int)  – kept for group compatibility (unused by FCFS)

    Returns
    -------
    results             : list of dict  – per-process computed metrics
    avg_waiting_time    : float
    avg_turnaround_time : float
    """
    n = len(processes)
    # sort by arrival time; tie-break by PID so output is deterministic
    procs = sorted(processes, key=lambda p: (p['arrival'], p['pid']))

    completed = []
    current_time = 0

    for proc in procs:
        # if CPU finished early and next process hasn't arrived yet, jump ahead
        if current_time < proc['arrival']:
            current_time = proc['arrival']

        start_time      = current_time
        finish_time     = start_time + proc['burst']
        turnaround_time = finish_time - proc['arrival']
        waiting_time    = turnaround_time - proc['burst']
        current_time    = finish_time

        completed.append({
            'pid'            : proc['pid'],
            'arrival'        : proc['arrival'],
            'burst'          : proc['burst'],
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

def print_results(results, avg_wt, avg_tat, title="FCFS (Non-Preemptive)"):
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
#    priority – used by Priority Scheduling teammates; FCFS ignores it

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

    # Test 1: All arrive at t=0 — order by PID
    # FCFS sorted by (arrival=0, pid) -> P1, P2, P3, P4
    # P1: start=0,  fin=6,  TAT=6,  WT=0
    # P2: start=6,  fin=14, TAT=14, WT=6
    # P3: start=14, fin=16, TAT=16, WT=14
    # P4: start=16, fin=20, TAT=20, WT=16
    # Avg WT=(0+6+14+16)/4=9.00, Avg TAT=(6+14+16+20)/4=14.00
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

    # Test 2: Staggered arrivals
    # FCFS order by arrival: P1(0) -> P2(1) -> P3(2) -> P4(3)
    # P1: start=0,  fin=6,  TAT=6,  WT=0
    # P2: start=6,  fin=14, TAT=13, WT=5
    # P3: start=14, fin=21, TAT=19, WT=12
    # P4: start=21, fin=24, TAT=21, WT=18
    # Avg WT=(0+5+12+18)/4=8.75, Avg TAT=(6+13+19+21)/4=14.75
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

    # Test 3: CPU idle gap
    # P1 finishes at t=4, P2 doesn't arrive until t=7 -> CPU sits idle
    # P1: start=0,  fin=4,  TAT=4,  WT=0
    # P2: start=7,  fin=15, TAT=8,  WT=0
    # P3: start=15, fin=20, TAT=10, WT=5
    # Avg WT=(0+0+5)/3=1.67, Avg TAT=(4+8+10)/3=7.33
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

    # Test 4: Tie on arrival — broken by PID
    # All arrive at t=0, sorted by PID: P1 -> P2 -> P3
    # P1: start=0,  fin=5,  TAT=5,  WT=0
    # P2: start=5,  fin=10, TAT=10, WT=5
    # P3: start=10, fin=14, TAT=14, WT=10
    # Avg WT=(0+5+10)/3=5.00, Avg TAT=(5+10+14)/3=9.67
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
    # Sorted by arrival: P1(0)->P2(2)->P3(4)->P4(4)->P5(6)->P6(8)
    # P3 and P4 tie on arrival=4, broken by PID so P3 before P4
    # P1: start=0,  fin=10, TAT=10, WT=0
    # P2: start=10, fin=11, TAT=9,  WT=8
    # P3: start=11, fin=16, TAT=12, WT=7
    # P4: start=16, fin=19, TAT=15, WT=12
    # P5: start=19, fin=26, TAT=20, WT=13
    # P6: start=26, fin=28, TAT=20, WT=18
    # Avg WT=(0+8+7+12+13+18)/6=9.67, Avg TAT=(10+9+12+15+20+20)/6=14.33
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


# ──────────────────────────────────────────────────────────────────────────────
#  Entry point
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # 1) Run on the shared group process set (required for project comparison)
    print("\n" + "#" * 56)
    print("  SHARED GROUP PROCESS SET — FCFS Non-Preemptive")
    print("#" * 56)
    results, avg_wt, avg_tat = fcfs(SHARED_PROCESSES)
    print_results(results, avg_wt, avg_tat,
                  title="FCFS (Non-Preemptive) — Group Comparison")

    # 2) Run the full test suite
    print("\n" + "#" * 56)
    print("  RUNNING TEST SUITE")
    print("#" * 56)
    run_all_tests()
