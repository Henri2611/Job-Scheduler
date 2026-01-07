import time
from concurrent.futures import ThreadPoolExecutor

# ---------------- TASK DEFINITIONS ----------------

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def heavy_task(n):
    s = 0
    for i in range(n):
        s += i*i
    return s

# ---------------- JOB EXECUTION ----------------

def execute_job(job_id, job_type, value):
    start = time.time()

    if job_type == "prime":
        result = is_prime(value)
    elif job_type == "compute":
        result = heavy_task(value)
    else:
        result = "Unknown task"

    end = time.time()
    print(f" Worker finished Job {job_id} ({job_type}) in {round(end-start, 3)}s")
    return result

# ---------------- SCHEDULERS ----------------

def sequential_scheduler(jobs):
    print("\n Running SEQUENTIALLY...\n")
    start = time.time()

    for job in jobs:
        job_id, job_type, value = job
        execute_job(job_id, job_type, value)

    end = time.time()
    total = end - start
    print(f"\n Sequential time: {round(total, 3)} seconds\n")
    return total

def parallel_scheduler(jobs, num_workers):
    print(f"\n Running in PARALLEL using {num_workers} workers...\n")
    start = time.time()

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for job in jobs:
            job_id, job_type, value = job
            futures.append(executor.submit(execute_job, job_id, job_type, value))

        for f in futures:
            f.result()

    end = time.time()
    total = end - start
    print(f"\n Parallel time: {round(total, 3)} seconds\n")
    return total

# ---------------- MENU SYSTEM ----------------

def menu():
    jobs = []
    job_counter = 1

    while True:
        print("\n====== PARALLEL AND SEQUENTIAL JOB SCHEDULER ======")
        print("1. Add compute task (heavy math)")
        print("2. Add prime-check task")
        print("3. View job list")
        print("4. Run sequential execution")
        print("5. Run parallel execution")
        print("6. Clear jobs")
        print("7. Exit")
        print("====================================")

        choice = input("Enter choice: ")

        # -------- ADD COMPUTE TASK --------
        if choice == "1":
            n = int(input("Enter number size (e.g., 50000): "))
            jobs.append((job_counter, "compute", n))
            print(f" Job {job_counter} added (compute up to {n})")
            job_counter += 1

        # -------- ADD PRIME TASK --------
        elif choice == "2":
            n = int(input("Enter number to test for primality: "))
            jobs.append((job_counter, "prime", n))
            print(f" Job {job_counter} added (prime test: {n})")
            job_counter += 1

        # -------- VIEW JOB LIST --------
        elif choice == "3":
            if not jobs:
                print(" No jobs in queue!.")
            else:
                print("\nCurrent jobs:")
                for j in jobs:
                    print(j)

        # -------- RUN SEQUENTIAL --------
        elif choice == "4":
            if not jobs:
                print(" Add jobs first!")
            else:
                Ts = sequential_scheduler(jobs)

        # -------- RUN PARALLEL --------
        elif choice == "5":
            if not jobs:
                print(" Add jobs first!")
            else:
                workers = int(input("Enter number of worker threads: "))
                Tp = parallel_scheduler(jobs, workers)

                Ts = sequential_scheduler(jobs)
                if Tp == 0:
                    print("\nParallel time was too small to measure accurately (≈0). Speedup cannot be computed.")
                else:
                    speedup = Ts / Tp
                    print(f"\nSpeedup = {speedup:.2f}x")

                    efficiency = speedup / workers

                    print("------ PERFORMANCE METRICS ------")
                    print(f"Speedup = {round(speedup, 3)}")
                    print(f"Efficiency = {round(efficiency, 3)}")
                    print("---------------------------------")

        # -------- CLEAR JOBS --------
        elif choice == "6":
            jobs = []
            job_counter = 1
            print(" Jobs cleared")

        # -------- EXIT --------
        elif choice == "7":
            print("Exiting... ")
            break

        else:
            print(" Invalid option. Try again.")

# ---------------- MAIN ----------------

if __name__ == "__main__":
    menu()
