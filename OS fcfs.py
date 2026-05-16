class Task:
    def __init__(self, task_id, arrival, burst):
        self.task_id = task_id
        self.arrival = arrival
        self.burst = burst


def first_come_first_serve(tasks):
    tasks.sort(key=lambda x: x.arrival)

    current_time = 0
    total_wait_time = 0
    total_turnaround_time = 0

    print("Task\tArrival\tBurst\tWait\tTurnaround")

    for task in tasks:
        wait_time = max(0, current_time - task.arrival)
        completion_time = current_time + task.burst
        turnaround_time = completion_time - task.arrival

        total_wait_time += wait_time
        total_turnaround_time += turnaround_time

        
        print(f"{task.task_id}\t{task.arrival}\t{task.burst}\t{wait_time}\t{turnaround_time}")

        current_time = completion_time

    print(f"Average waiting time: {total_wait_time / len(tasks):.2f}")
    print(f"Average turnaround time: {total_turnaround_time / len(tasks):.2f}")


if __name__ == "__main__":
    tasks = [
        Task(1, 0, 8),
        Task(3, 2, 9),
        Task(2, 1, 4),
        Task(4, 3, 5)
    ]
    first_come_first_serve(tasks)