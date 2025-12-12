import csv
import streamlit as st
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


def get_scheduler(name, processes, quantum):
    if name == "FCFS":
        return FCFSScheduler(processes)
    if name == "SJF (Preemptive)":
        return SJFPreemptiveScheduler(processes)
    if name == "SJF (Non-Preemptive)":
        return SJFNonPreemptiveScheduler(processes)
    if name == "Round Robin":
        return RoundRobinScheduler(processes, quantum)
    if name == "Priority (Preemptive)":
        return PriorityPreemptiveScheduler(processes)
    if name == "Priority (Non-Preemptive)":
        return PriorityNonPreemptiveScheduler(processes)
    return None


def main():
    st.set_page_config(page_title="EBLG341 CPU Scheduler Raporu", layout="wide")

    st.title("EBLG341 – CPU Zamanlama Raporu")
    st.write("Verilen iki veri seti üzerinde farklı CPU zamanlama algoritmalarının sonuçlarını incelemek için bu arayüzü kullanabilirsiniz.")

    col1, col2 = st.columns(2)
    with col1:
        dataset = st.selectbox("Veri seti", ["case1", "case2"])
    with col2:
        algo_name = st.selectbox(
            "Algoritma",
            [
                "FCFS",
                "SJF (Preemptive)",
                "SJF (Non-Preemptive)",
                "Round Robin",
                "Priority (Preemptive)",
                "Priority (Non-Preemptive)",
            ],
        )

    quantum = 4
    if algo_name == "Round Robin":
        quantum = st.slider("Round Robin quantum", min_value=1, max_value=10, value=4, step=1)

    if dataset == "case1":
        data_path = "data/data1.csv"
    else:
        data_path = "data/data2.csv"

    if st.button("Çalıştır"):
        processes = load_processes(data_path)
        scheduler = get_scheduler(algo_name, processes, quantum)
        if scheduler is None:
            st.error("Algoritma seçimi geçersiz.")
            return
        result = scheduler.run()

        st.subheader("Zaman Çizelgesi")
        seg_rows = []
        for start, label, end in result["segments"]:
            seg_rows.append(
                {
                    "Başlangıç Zamanı": start,
                    "Süreç": label,
                    "Bitiş Zamanı": end,
                }
            )
        st.dataframe(seg_rows, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("Bekleme Süreleri")
            st.write(f"Maksimum Bekleme Süresi: {result['max_waiting']}")
            st.write(f"Ortalama Bekleme Süresi: {result['avg_waiting']:.3f}")
            st.subheader("Turnaround Süreleri")
            st.write(f"Maksimum Turnaround Süresi: {result['max_turnaround']}")
            st.write(f"Ortalama Turnaround Süresi: {result['avg_turnaround']:.3f}")
        with col_b:
            st.subheader("CPU Verimliliği ve Bağlam Değiştirme")
            st.write(f"Toplam Bağlam Değiştirme Sayısı: {result['context_switches']}")
            st.write(f"CPU Verimliliği: {result['cpu_utilization']:.3f}")
            st.subheader("Throughput")
            for T, count in result["throughputs"].items():
                st.write(f"T = {T} için tamamlanan süreç sayısı: {count}")


if __name__ == "__main__":
    main()
