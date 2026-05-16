from collections import deque

class Task:
    def __init__(self, task_id, arrival_time, burst_time):
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.start_time = None
        self.finish_time = None

def round_robin(tasks, quantum):
    
    tasks.sort(key=lambda x: x.arrival_time)

    ready_queue = deque()
    current_time = 0
    index = 0

    
    while index < len(tasks) and tasks[index].arrival_time <= current_time:
        ready_queue.append(tasks[index])
        index += 1

    while ready_queue:
        task = ready_queue.popleft()

        if task.start_time is None:
            task.start_time = current_time

        if task.remaining_time > quantum:
            current_time += quantum
            task.remaining_time -= quantum

        
            while index < len(tasks) and tasks[index].arrival_time <= current_time:
                ready_queue.append(tasks[index])
                index += 1

            ready_queue.append(task)
        else:
            current_time += task.remaining_time
            task.remaining_time = 0
            task.finish_time = current_time

            while index < len(tasks) and tasks[index].arrival_time <= current_time:
                ready_queue.append(tasks[index])
                index += 1

    
        if not ready_queue and index < len(tasks):
            current_time = tasks[index].arrival_time
            while index < len(tasks) and tasks[index].arrival_time <= current_time:
                ready_queue.append(tasks[index])
                index += 1

    print("Process ID\tWaiting Time\tTurnaround Time\tResponse Time")
    total_wait = total_turnaround = total_response = 0

    for task in tasks:
        turnaround = task.finish_time - task.arrival_time
        waiting = turnaround - task.burst_time
        response = task.start_time - task.arrival_time

        total_wait += waiting
        total_turnaround += turnaround
        total_response += response

        print(f"{task.task_id}\t\t{waiting}\t\t{turnaround}\t\t{response}")

    n = len(tasks)
    print(f"Average waiting time: {total_wait / n:.2f}")
    print(f"Average turnaround time: {total_turnaround / n:.2f}")
    print(f"Average response time: {total_response / n:.2f}")

if __name__ == "__main__":
    tasks = [
        Task(1, 0, 8),
        Task(3, 2, 9),
        Task(2, 1, 4),
        Task(4, 3, 5),
    ]
    round_robin(tasks, 3)