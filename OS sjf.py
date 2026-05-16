class ProcessInfo:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

def sjf_non_preemptive(processes):
    current_time = 0
    completed = []
    remaining = processes[:]

    while remaining:
        available = [p for p in remaining if p.arrival_time <= current_time]

        if not available:
            current_time = min(p.arrival_time for p in remaining)
            available = [p for p in remaining if p.arrival_time <= current_time]

        process = min(available, key=lambda p: p.burst_time)

        process.start_time = current_time
        process.finish_time = current_time + process.burst_time
        process.turnaround_time = process.finish_time - process.arrival_time
        process.waiting_time = process.start_time - process.arrival_time
        process.response_time = process.waiting_time

        current_time = process.finish_time
        completed.append(process)
        remaining.remove(process)

    print("\nSJF scheduling algorithm\n")
    print("Process ID\tWaiting Time\tTurnaround Time\tResponse Time")

    total_wait = total_turnaround = total_response = 0

    for p in completed:
        total_wait += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += p.response_time

        print(f"{p.pid}\t\t{p.waiting_time}\t\t{p.turnaround_time}\t\t{p.response_time}")

    n = len(completed)
    print(f"\nAverage waiting time: {total_wait / n:.2f}")
    print(f"Average turnaround time: {total_turnaround / n:.2f}")
    print(f"Average response time: {total_response / n:.2f}")

if __name__ == "__main__":
    processes = [
        ProcessInfo("P1", 0, 8),
        ProcessInfo("P2", 2, 9),
        ProcessInfo("P3", 1, 4),
        ProcessInfo("P4", 3, 5),
    ]

    sjf_non_preemptive(processes)