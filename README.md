
# Parallel & Distributed Job Scheduler (Python)

This project implements a hybrid job scheduling system that demonstrates:

- sequential execution
- parallel execution using multiprocessing
- distributed execution using simulated worker nodes

Users can add computational jobs, execute them using different execution models, and measure performance improvements such as speedup and efficiency.

## System Overview

The program supports three execution modes:

- Sequential: jobs run one after another on a single CPU
- Parallel: jobs run simultaneously across CPU cores using multiprocessing
- Distributed: jobs are sent to multiple simulated nodes (separate processes)

The system uses ProcessPoolExecutor for parallel CPU execution and multiprocessing.Process + Queue to simulate distributed nodes.

## Screenshot — Menu

A command-line menu interface is used to interact with the scheduler. Link to the menu image:

[Menu Screenshot](menu.png)

Example menu layout:

```
=========== PARALLEL & DISTRIBUTED JOB SCHEDULER ===========
1. Add compute task (heavy math)
2. View job queue
3. Run sequential execution
4. Run parallel execution (multiprocessing)
5. Run distributed execution (multi-node simulation)
6. Clear job queue
7. Exit
=============================================================
```

## Features

- Interactive command-line interface
- Add multiple compute-intensive jobs
- Three execution models: sequential, parallel multiprocessing, distributed simulated nodes
- Performance evaluation: sequential time, parallel time, speedup, efficiency
- Clear jobs and rerun experiments

## Tasks Supported

Workload: a CPU-intensive mathematical task (sum of squares loop) that scales with N. This provides a controlled synthetic workload suitable for benchmarking.

## Dataset Used

No external datasets are required. The project uses synthetic numeric workloads (integer N denoting computation size).

Example job: "compute heavy task with N = 200000".

## Requirements

- Python 3.8 or higher
- Standard library modules: multiprocessing, concurrent.futures, time

Works on Windows, Linux, and macOS. No external pip packages required.

## How to Run

1. Ensure the script is saved as scheduler.py (or run job_scheduler.py if present).
2. Open a terminal in the project directory.

Windows:
```
cd path\to\folder
python scheduler.py
```

Linux / macOS:
```
cd /path/to/folder
python3 scheduler.py
```

The interactive menu will start. No compilation is required.

## Usage Instructions

Menu options:

1. Add compute task — specify computation size (e.g., 200000)
2. View job queue — displays pending jobs
3. Run sequential execution — baseline performance
4. Run parallel execution — uses multiple CPU cores; reports speedup and efficiency
5. Run distributed execution — jobs assigned to simulated nodes
6. Clear job queue
7. Exit

## Performance Metrics Explained

After running in parallel mode, the program runs sequentially to compare:

- Speedup = sequential_time / parallel_time
- Efficiency = speedup / number_of_workers

These metrics help evaluate parallel scaling.

## Educational Objectives

This project demonstrates:

- job scheduling
- CPU parallelism using multiprocessing
- distributed execution concepts via simulated nodes
- load distribution and performance benchmarking

## Weekly Progress Summary (4 Weeks)

Week 1 — Task Analysis & Design
- identified requirements and workload
- designed job queue, worker model, and menu interface

Week 2 — Parallel Implementation
- implemented sequential scheduler and multiprocessing parallel scheduler
- tested CPU-bound execution and collected baseline timings

Week 3 — Distributed Simulation
- implemented simulated nodes using processes and a task queue
- added node shutdown logic and tested distributed behavior

Week 4 — Integration & Evaluation
- integrated schedulers into a menu system
- added performance reporting and tested with varying workload sizes

## Limitations

- Distributed nodes are simulated on a single machine (no network)
- Uses processes rather than networked machines
- CPU-bound tasks may be affected by system scheduling and available cores

## License

Free for education and personal learning purposes.
  
