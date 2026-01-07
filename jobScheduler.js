// ------------------------------
// Job Model
// ------------------------------
class Job {
  constructor(id, duration) {
    this.id = id;
    this.duration = duration;
    this.status = "queued"; // queued | running | completed | failed
    this.result = null;
    this.startTime = null;
    this.endTime = null;
  }

  async execute() {
    this.status = "running";
    this.startTime = Date.now();

    return new Promise((resolve) => {
      setTimeout(() => {
        this.endTime = Date.now();
        this.status = "completed";
        this.result = `Job ${this.id} completed in ${this.duration}ms`;
        resolve(this.result);
      }, this.duration);
    });
  }
}

// ------------------------------
// Message Queue (Distributed Simulation)
// ------------------------------
class MessageQueue {
  constructor() {
    this.queue = [];
  }

  push(msg) {
    this.queue.push(msg);
  }

  pop() {
    return this.queue.shift();
  }
}

// ------------------------------
// Worker Node (Distributed Worker)
// ------------------------------
class Worker {
  constructor(id, failureProbability = 0.1) {
    this.id = id;
    this.isBusy = false;
    this.alive = true;
    this.failureProbability = failureProbability;
    this.lastHeartbeat = Date.now();
  }

  heartbeat() {
    if (!this.alive) return;
    this.lastHeartbeat = Date.now();
  }

  // simulate random crash
  maybeFail() {
    if (Math.random() < this.failureProbability) {
      console.log(`❌ Worker ${this.id} failed`);
      this.alive = false;
      this.isBusy = false;
    }
  }

  async run(job) {
    this.isBusy = true;
    console.log(`Worker ${this.id} running Job ${job.id}`);

    this.maybeFail();
    if (!this.alive) throw new Error("Worker crashed");

    const result = await job.execute();

    this.isBusy = false;
    return result;
  }
}

// ------------------------------
// Scheduler (Master Node)
// ------------------------------
class Scheduler {
  constructor(workers, policy = "roundrobin") {
    this.workers = workers;
    this.jobQueue = [];
    this.completedJobs = [];
    this.policy = policy;
    this.roundIndex = 0;

    this.messageQueue = new MessageQueue();
    this.checkpoint = [];
  }

  submitJob(job) {
    this.jobQueue.push(job);
    this.saveCheckpoint();
    this.assignJobs();
  }

  // load balancing strategies
  chooseWorker() {
    const alive = this.workers.filter(w => w.alive && !w.isBusy);
    if (alive.length === 0) return null;

    switch (this.policy) {
      case "random":
        return alive[Math.floor(Math.random() * alive.length)];

      case "roundrobin":
        const w = alive[this.roundIndex % alive.length];
        this.roundIndex++;
        return w;

      default:
        return alive[0];
    }
  }

  assignJobs() {
    while (this.jobQueue.length > 0) {
      const worker = this.chooseWorker();
      if (!worker) return;

      const job = this.jobQueue.shift();
      this.executeJob(worker, job);
    }
  }

  async executeJob(worker, job) {
    try {
      const result = await worker.run(job);
      console.log(`✔️ ${result}`);
      this.completedJobs.push(job);
    } catch (err) {
      console.log(`⚠️ Job ${job.id} failed — requeued`);
      job.status = "queued";
      this.jobQueue.push(job);
    } finally {
      this.assignJobs();
    }
  }

  // ------------------------------
  // Heartbeat + failure recovery
  // ------------------------------
  monitorWorkers() {
    setInterval(() => {
      const now = Date.now();

      for (const worker of this.workers) {
        if (!worker.alive) {
          console.log(`♻️ Recovering worker ${worker.id}`);
          worker.alive = true;
        }

        // simulate heartbeat
        worker.heartbeat();

        // detect unresponsive worker
        if (now - worker.lastHeartbeat > 3000) {
          console.log(`❌ Worker ${worker.id} unresponsive`);
          worker.alive = false;
        }
      }
    }, 1000);
  }

  // ------------------------------
  // Checkpointing
  // ------------------------------
  saveCheckpoint() {
    this.checkpoint = this.jobQueue.map(j => ({ id: j.id, status: j.status }));
  }
}

// ------------------------------
// Experiment / Demo
// ------------------------------
const workers = [
  new Worker(1),
  new Worker(2),
  new Worker(3),
];

const scheduler = new Scheduler(workers, "roundrobin");
scheduler.monitorWorkers();

// dataset (Week 1 requirement)
let jobId = 1;
const durations = [300, 700, 1200, 500, 2000, 900, 400];

durations.forEach(d => scheduler.submitJob(new Job(jobId++, d)));
