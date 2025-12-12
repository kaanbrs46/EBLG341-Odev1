class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority
        self.completion_time = None

    def copy(self):
        return Process(self.pid, self.arrival_time, self.burst_time, self.priority)


class CpuScheduler:
    def __init__(self, processes):
        self.processes = processes

    def clone_processes(self):
        return [p.copy() for p in self.processes]

    def build_result(self, ticks, processes):
        idle = sum(1 for x in ticks if x is None)
        total_time = len(ticks)
        cpu_busy = total_time - idle
        context_switches = 0
        for i in range(1, len(ticks)):
            if (
                ticks[i] != ticks[i - 1]
                and ticks[i] is not None
                and ticks[i - 1] is not None
            ):
                context_switches += 1
        segments = []
        if ticks:
            start = 0
            current = ticks[0]
            for i in range(1, len(ticks)):
                if ticks[i] != current:
                    label = "IDLE" if current is None else current
                    segments.append((start, label, i))
                    start = i
                    current = ticks[i]
            label = "IDLE" if current is None else current
            segments.append((start, label, len(ticks)))
        turnaround = {}
        waiting = {}
        for p in processes:
            if p.completion_time is None:
                continue
            ta = p.completion_time - p.arrival_time
            wt = ta - p.burst_time
            turnaround[p.pid] = ta
            waiting[p.pid] = wt
        max_turnaround = max(turnaround.values()) if turnaround else 0
        avg_turnaround = sum(turnaround.values()) / len(turnaround) if turnaround else 0
        max_waiting = max(waiting.values()) if waiting else 0
        avg_waiting = sum(waiting.values()) / len(waiting) if waiting else 0
        throughputs = {}
        for T in [50, 100, 150, 200]:
            count = 0
            for p in processes:
                if p.completion_time is not None and p.completion_time <= T:
                    count += 1
            throughputs[T] = count
        overhead_per_switch = 0.001
        real_time = total_time + context_switches * overhead_per_switch
        if real_time > 0:
            cpu_utilization = cpu_busy / real_time
        else:
            cpu_utilization = 0.0
        return {
            "segments": segments,
            "max_waiting": max_waiting,
            "avg_waiting": avg_waiting,
            "max_turnaround": max_turnaround,
            "avg_turnaround": avg_turnaround,
            "throughputs": throughputs,
            "cpu_utilization": cpu_utilization,
            "context_switches": context_switches,
        }


class FCFSScheduler(CpuScheduler):
    def run(self):
        procs = sorted(self.clone_processes(), key=lambda p: p.arrival_time)
        n = len(procs)
        time = 0
        ticks = []
        completed = 0
        current = None
        while completed < n:
            ready = [
                p
                for p in procs
                if p.arrival_time <= time
                and p.completion_time is None
                and p.remaining_time > 0
            ]
            if current is None and ready:
                ready.sort(key=lambda p: p.arrival_time)
                current = ready[0]
            if current is None and not ready:
                if any(p.completion_time is None for p in procs):
                    ticks.append(None)
                    time += 1
                    continue
                else:
                    break
            ticks.append(current.pid)
            current.remaining_time -= 1
            time += 1
            if current.remaining_time == 0:
                current.completion_time = time
                completed += 1
                current = None
        return self.build_result(ticks, procs)


class SJFPreemptiveScheduler(CpuScheduler):
    def run(self):
        procs = sorted(self.clone_processes(), key=lambda p: p.arrival_time)
        n = len(procs)
        time = 0
        ticks = []
        completed = 0
        while completed < n:
            ready = [
                p
                for p in procs
                if p.arrival_time <= time
                and p.completion_time is None
                and p.remaining_time > 0
            ]
            if not ready:
                if any(p.completion_time is None for p in procs):
                    ticks.append(None)
                    time += 1
                    continue
                else:
                    break
            current = min(ready, key=lambda p: (p.remaining_time, p.arrival_time))
            ticks.append(current.pid)
            current.remaining_time -= 1
            time += 1
            if current.remaining_time == 0:
                current.completion_time = time
                completed += 1
        return self.build_result(ticks, procs)


class SJFNonPreemptiveScheduler(CpuScheduler):
    def run(self):
        procs = sorted(self.clone_processes(), key=lambda p: p.arrival_time)
        n = len(procs)
        time = 0
        ticks = []
        completed = 0
        while completed < n:
            ready = [
                p
                for p in procs
                if p.arrival_time <= time
                and p.completion_time is None
                and p.remaining_time > 0
            ]
            if not ready:
                if any(p.completion_time is None for p in procs):
                    ticks.append(None)
                    time += 1
                    continue
                else:
                    break
            current = min(ready, key=lambda p: (p.burst_time, p.arrival_time))
            while current.remaining_time > 0:
                ticks.append(current.pid)
                current.remaining_time -= 1
                time += 1
            current.completion_time = time
            completed += 1
        return self.build_result(ticks, procs)


class RoundRobinScheduler(CpuScheduler):
    def __init__(self, processes, quantum):
        super().__init__(processes)
        self.quantum = quantum

    def run(self):
        procs = sorted(self.clone_processes(), key=lambda p: p.arrival_time)
        n = len(procs)
        time = 0
        ticks = []
        completed = 0
        i = 0
        ready_queue = []
        current = None
        quantum_left = 0
        while completed < n:
            while i < n and procs[i].arrival_time <= time:
                ready_queue.append(procs[i])
                i += 1
            if current is None:
                if ready_queue:
                    current = ready_queue.pop(0)
                    quantum_left = self.quantum
                else:
                    if any(p.completion_time is None for p in procs):
                        ticks.append(None)
                        time += 1
                        continue
                    else:
                        break
            ticks.append(current.pid)
            current.remaining_time -= 1
            quantum_left -= 1
            time += 1
            if current.remaining_time == 0:
                current.completion_time = time
                completed += 1
                current = None
                quantum_left = 0
            elif quantum_left == 0:
                while i < n and procs[i].arrival_time <= time:
                    ready_queue.append(procs[i])
                    i += 1
                ready_queue.append(current)
                current = None
        return self.build_result(ticks, procs)


class PriorityPreemptiveScheduler(CpuScheduler):
    def run(self):
        procs = sorted(self.clone_processes(), key=lambda p: p.arrival_time)
        n = len(procs)
        time = 0
        ticks = []
        completed = 0
        while completed < n:
            ready = [
                p
                for p in procs
                if p.arrival_time <= time
                and p.completion_time is None
                and p.remaining_time > 0
            ]
            if not ready:
                if any(p.completion_time is None for p in procs):
                    ticks.append(None)
                    time += 1
                    continue
                else:
                    break
            current = min(ready, key=lambda p: (p.priority, p.arrival_time))
            ticks.append(current.pid)
            current.remaining_time -= 1
            time += 1
            if current.remaining_time == 0:
                current.completion_time = time
                completed += 1
        return self.build_result(ticks, procs)


class PriorityNonPreemptiveScheduler(CpuScheduler):
    def run(self):
        procs = sorted(self.clone_processes(), key=lambda p: p.arrival_time)
        n = len(procs)
        time = 0
        ticks = []
        completed = 0
        while completed < n:
            ready = [
                p
                for p in procs
                if p.arrival_time <= time
                and p.completion_time is None
                and p.remaining_time > 0
            ]
            if not ready:
                if any(p.completion_time is None for p in procs):
                    ticks.append(None)
                    time += 1
                    continue
                else:
                    break
            current = min(ready, key=lambda p: (p.priority, p.arrival_time))
            while current.remaining_time > 0:
                ticks.append(current.pid)
                current.remaining_time -= 1
                time += 1
            current.completion_time = time
            completed += 1
        return self.build_result(ticks, procs)
