import csv
import os
from schedulers import (
    Process,
    FCFSScheduler,
    SJFPreemptiveScheduler,
    SJFNonPreemptiveScheduler,
    RoundRobinScheduler,
    PriorityPreemptiveScheduler,
    PriorityNonPreemptiveScheduler,
)

PRIORITY_MAP = {
    "high": 1,
    "normal": 2,
    "low": 3,
}


def load_processes(path):
    processes = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return processes

    header_row = rows[0]
    data_rows = rows[1:]

    if len(header_row) == 1 and "," in header_row[0]:
        header_text = header_row[0].strip().strip('"')
        header = [h.strip() for h in header_text.split(",")]

        fixed_data_rows = []
        for row in data_rows:
            if not row:
                continue
            cell = row[0].strip().strip('"')
            cols = [c.strip() for c in cell.split(",")]
            fixed_data_rows.append(cols)
        data_rows = fixed_data_rows
    else:
        header = [h.strip() for h in header_row]
        data_rows = [[c.strip() for c in row] for row in data_rows]

    idx_pid = header.index("Process_ID")
    idx_arrival = header.index("Arrival_Time")
    idx_burst = header.index("CPU_Burst_Time")
    idx_priority = header.index("Priority")

    for row in data_rows:
        if not row or len(row) <= max(idx_pid, idx_arrival, idx_burst, idx_priority):
            continue
        pid = row[idx_pid]
        arrival = int(row[idx_arrival])
        burst = int(row[idx_burst])
        priority_str = row[idx_priority].strip().lower()
        prio = PRIORITY_MAP[priority_str]
        processes.append(Process(pid, arrival, burst, prio))

    return processes



def write_result(name, case_name, result):
    if not os.path.exists("output"):
        os.makedirs("output")
    out_path = os.path.join("output", f"{name}_{case_name}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        for start, label, end in result["segments"]:
            f.write(f"[ {start} ] - - {label} - - [ {end} ]\n")
        f.write("\nMETRICS\n")
        f.write(f"Max Waiting Time: {result['max_waiting']}\n")
        f.write(f"Avg Waiting Time: {result['avg_waiting']}\n")
        f.write(f"Max Turnaround Time: {result['max_turnaround']}\n")
        f.write(f"Avg Turnaround Time: {result['avg_turnaround']}\n")
        f.write(f"Context Switches: {result['context_switches']}\n")
        f.write(f"CPU Utilization: {result['cpu_utilization']}\n")
        f.write("Throughput (completed by T):\n")
        for T, count in result["throughputs"].items():
            f.write(f"T = {T}: {count}\n")


def run_all_for_case(case_name, file_path, quantum=4):
    processes = load_processes(file_path)
    algos = [
        ("fcfs", FCFSScheduler(processes)),
        ("sjf_preemptive", SJFPreemptiveScheduler(processes)),
        ("sjf_nonpreemptive", SJFNonPreemptiveScheduler(processes)),
        ("rr", RoundRobinScheduler(processes, quantum)),
        ("priority_preemptive", PriorityPreemptiveScheduler(processes)),
        ("priority_nonpreemptive", PriorityNonPreemptiveScheduler(processes)),
    ]
    for name, scheduler in algos:
        result = scheduler.run()
        write_result(name, case_name, result)


def main():
    run_all_for_case("case1", "data/data1.csv", quantum=4)
    run_all_for_case("case2", "data/data2.csv", quantum=4)


if __name__ == "__main__":
    main()
