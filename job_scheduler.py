import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Queue, cpu_count

# =====================================================
#                     TASK
# =====================================================

def heavy_task(n):
    """
    Simple CPU-intensive computation to simulate workload.
    """
    s = 0
    for i in range(n):
        s += i * i
    return s


# =====================================================
#              JOB EXECUTION FUNCTION
# =====================================================

def execute_job(job_id, value):
    start = time.time()

    result = heavy_task(value)

    end = time.time()
    print(f" Worker finished Job {job_id} in {round(end-start,3)}s")
    return result


# =====================================================
#           SEQUENTIAL SCHEDULER (BASELINE)
# =====================================================

def sequential_scheduler(jobs):
    print("\n Running SEQUENTIALLY...\n")
    start = time.time()

    for job in jobs:
        job_id, value = job
        execute_job(job_id, value)

    total = time.time() - start
    print(f"\n Sequential execution time = {round(total,3)} seconds\n")
    return total


# =====================================================
#        PARALLEL SCHEDULER (MULTIPROCESSING)
# =====================================================

def parallel_scheduler(jobs, num_workers):
    print(f"\n Running PARALLEL execution with {num_workers} workers...\n")

    start = time.time()

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for job in jobs:
            job_id, value = job
            futures.append(executor.submit(execute_job, job_id, value))

        for f in futures:
            f.result()

    total = time.time() - start
    print(f"\n Parallel execution time = {round(total,3)} seconds\n")
    return total


# =====================================================
#           DISTRIBUTED NODE SIMULATION
# =====================================================

def worker_node(node_id, task_queue):
    while True:
        job = task_queue.get()

        if job is None:
            print(f" Node {node_id} shutting down.")
            break

        job_id, value = job
        print(f" Node {node_id} received Job {job_id}")
        execute_job(job_id, value)


def distributed_scheduler(jobs, num_nodes):
    print(f"\n Running DISTRIBUTED execution on {num_nodes} nodes...\n")

    task_queue = Queue()

    nodes = []
    for n in range(num_nodes):
        p = Process(target=worker_node, args=(n+1, task_queue))
        p.start()
        nodes.append(p)

    for job in jobs:
        task_queue.put(job)

    for _ in range(num_nodes):
        task_queue.put(None)

    for p in nodes:
        p.join()

    print("\n Distributed execution complete.\n")


# =====================================================
#                     MENU SYSTEM
# =====================================================

def menu():
    jobs = []
    job_counter = 1

    while True:
        print("\n=========== PARALLEL & DISTRIBUTED JOB SCHEDULER ===========")
        print("1. Add compute task (heavy math)")
        print("2. View job queue")
        print("3. Run sequential execution")
        print("4. Run parallel execution (multiprocessing)")
        print("5. Run distributed execution (multi-node simulation)")
        print("6. Clear job queue")
        print("7. Exit")
        print("=============================================================")

        choice = input("Enter choice: ")

        # ADD HEAVY COMPUTATION JOB
        if choice == "1":
            n = int(input("Enter computation size (e.g., 200000): "))
            jobs.append((job_counter, n))
            print(f" Job {job_counter} added (compute up to {n})")
            job_counter += 1

        # VIEW JOB QUEUE
        elif choice == "2":
            if not jobs:
                print(" No jobs in queue.")
            else:
                for j in jobs:
                    print(j)

        # SEQUENTIAL EXECUTION
        elif choice == "3":
            if not jobs:
                print(" Add jobs first!")
            else:
                sequential_scheduler(jobs)

        # PARALLEL EXECUTION
        elif choice == "4":
            if not jobs:
                print(" Add jobs first!")
            else:
                workers = int(input(f"Enter number of workers (1–{cpu_count()}): "))
                Tp = parallel_scheduler(jobs, workers)
                Ts = sequential_scheduler(jobs)

                speedup = Ts / Tp if Tp > 0 else 0
                efficiency = speedup / workers if workers > 0 else 0

                print("\n------ PERFORMANCE METRICS ------")
                print(f"Speedup      = {round(speedup,3)}x")
                print(f"Efficiency   = {round(efficiency*100,2)}%")
                print("---------------------------------\n")

        # DISTRIBUTED EXECUTION
        elif choice == "5":
            if not jobs:
                print(" Add jobs first!")
            else:
                nodes = int(input("Enter number of simulated nodes: "))
                distributed_scheduler(jobs, nodes)

        # CLEAR JOBS
        elif choice == "6":
            jobs = []
            job_counter = 1
            print(" Job queue cleared.")

        # EXIT
        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print(" Invalid choice.")


# =====================================================
#                        MAIN
# =====================================================

if __name__ == "__main__":
    menu()
