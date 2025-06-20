# Chaos Testing on a K3s (Kubernetes) Cluster

![alt text](https://github.com/siddhesh2263/chaos-testing/blob/main/assets/merged-logos.png?raw=true)

<br>

## What is chaos testing?

Chaos testing is the practice of deliberately injecting failures into a system to observe how it behaves under stress or partial outage. The goal is to identify weaknesses in the system and its recovery mechanisms — before real-world failures occur. Chaos testing helps surface hidden assumptions, brittle dependencies, and unmonitored failure modes.

<br>

## Key characteristics of chaos testing

### Controlled:
Failures are introduced in a known, observable way.

### Repeatable:
Scenarios can be replayed to verify fixes.

### Measured:
Metrics, logs, and alerts are used to assess system behaviour and overall impact.

### Incremental:
We can start with small faults, and then expans to compound failures.

<br>

## Examples of chaos experiments

### Pod failure:
In this case, we delete a pod mid-request. This is at the Kubernetes cluster level, caused as a result of some infrastructure problem. This tests the system's auto-healing property.

### Node unavailability:
A node is drained or shut down.

### Network delay/loss:
A time delay is injected, for example between the service writing data to a database (in this article we won't be dicussing this, since it requires sudo/root access on all the cluster nodes, which is something I'll do in a later series of articles.)

### Resource exhaustion:
A high CPU or memory load is simulated.

### Service crash:
This type of failure occurs inside the pod, and is application level. This type of failure tests the application's exception handling logic.

<br>

## Requirements to follow the guide

1. A working Kubernetes cluster with at least `3 nodes` (physical in my case, but can be virtual; I operate all my nodes in a headless manner.)
2. On the development machine, `kubectl` must be configured to access the Kubernetes cluster. I'm using a Windows machine as the development system, so `Git` is required to run the chaos testing scripts.
3. For this article, I've been using a set of microservices - a `gateway`, a `database writer` service, and an `user interface (UI)` service. There is no decoupling between the services, and they communicate with each other using `HTTP` (except the database connection.) The code and YAML files for them are uploaded in this repository.
4. To simulate the requests, I'm using `Locust`. The file is shared in this repository.
5. Since this is a Linux environment, the user needs to have knowledge of how to check CPU and memory usage, pod counts (all the basic Kubernetes commands,) and able to understand errors which they can troubleshoot.

<br>

## Brief introduction to auto scaling

In real world systems, application load is never constant - traffic spikes, sudden drops, and unpredictable behavior are common. Kubernetes handles this challenge by using the auto scaling property, which ensures applications scale up when there's a lot of requests, and scale down when the usage is idle. This optimizes both performance and resource costs.

Auto scaling in Kubernetes is driven by real time metrics such as CPU usage, memory consumption, or any other custom application metrics. When these metrics cross over the configured thresholds, Kubernetes adjusts the number of running pod replicas automatically. Our focus will be on one specific type of auto scaling, which is the `Horizontal Pod Autoscalar` (HPA.) The HPA scales the number of pod replicas depending on the CPU, memory, or custom metrics.

We used YAML files to run our application on the Kubernetes cluster. Along with this, we will create an additonal YAML file for HPA details. This contains the CPU or memory requests and limits for the deployment. Once this HPA policy is applied on the cluster, we can observe the auto scaling behavior based on load we would generate using Locust.

<br>

### How does it relate to chaos testing?

A combination of failures introduced by chaos testing, and a load of requests sent by Locust will generate stress on the system. Auto scaling responds to this stress, and provides us the details if the system can scale up fast enough to handle increased demand or resourc strain. Let's look at it in more detail:

### Scenario 1 - Kill a pod mid-request
When a pod goes down, the other services retry logic and overall fault tolerance of the system will be tested. In the meantime, HPA or the deployment tries to create a new pod.

### Scenario 2 - Drain a node during high load:
When this happens, the system's service availability will be checked. HPA may or may not be involved too much in this, since the node will be deemed unavailable, Kubernetes will try to host the pods on other nodes.

### Scenario 3 - Injection of high CPU/memory pressure:
The degradation in the application will be visible, and HPA in this case should be able to scale out the pods.

### Scenario 4 - Sudden surge in traffic:
A sudden surge in traffic will cause queue backlogs in the gateway, and will lead to an increase in response time. If thresholds are crossed in this scenario, HPA should increase replicas.

<br>

## Running different scenarios

We will look at one case which has a combination of multiple faults taking place one after another. The total script run time is close to `8 minutes`. Given this time, I ran Locust for around `10 minutes`. Below is the workflow of the chaos scenario:

<br>

![alt text](https://github.com/siddhesh2263/chaos-testing/blob/main/assets/script-flow-image.png?raw=true)


`Drain Node` temporarily removes a node from the cluster to test if workloads reschedule correctly.

`Delete Gateway Pod` simulates a sudden API service failure and ensures it's replaced by Kubernetes.

`Induce CrashLoop on Gateway` forces the gateway into a broken state to test failure detection and rollback procedures.

`Delete UI Pod` simulates frontend outage and tests recovery behavior for user-facing components.

`Scale Gateway to 10 Replicas` manually scales the gateway to test resource utilization and autoscaling behavior.

`Undo CrashLoop (Rollout Undo)` restores the broken gateway deployment to verify rollback and health restoration.

`Uncordon Node` brings the drained node back into the cluster to test node reintegration.

`Scale Gateway Down to 2 Replicas` reduces replicas to check clean scale-down and service continuity.

<br>

![alt text](https://github.com/siddhesh2263/chaos-testing/blob/main/assets/chaos-script-output.png?raw=true)

## Observations

Below image shows the reason for request failures. The error points to an application level crash or error, and is not a cluster problem. These errors are HTTP 500s, indicating that the gateway service was reachable but failed to process the requests - likely due to a dependency failure or application error.

![alt text](https://github.com/siddhesh2263/chaos-testing/blob/main/assets/all-failure-reason.png?raw=true)

<br>

Recall that we drained a node in the first stage. We can see on the `Lens` application (which is used to view Kubernetes related setup) that one of the nodes is disabled:

![alt text](https://github.com/siddhesh2263/chaos-testing/blob/main/assets/node-drain.png?raw=true)

<br>

Let's move on to the Locust report. It shows a grim picture - the system is not just failing, but it's struggling under load, and is taking a long time to respond before the HTTP 500 errors are returned. There can be many causes for it:
* Slow writes to the database could back up the entire gateway request flow,
* The Flask services are run on development configuration, and not Gunicorn. This means it's working as a single threaded application, and without the presence of workers or sync mode, it will queue up requests.
* The biggest problem could be the absence of timeout handling or retry logic in the application. If the request that's taking too long is stuck, it will result in a timeout, and as the client sees a slow HTTP 500 error, Locust logs it as a failure.

![alt text](https://github.com/siddhesh2263/chaos-testing/blob/main/assets/charts-locust-report.png?raw=true)

<br>

Once the chaos testing reaches the last stage, the node is uncordoned. The below image shows that the node is up again:

![alt text](https://github.com/siddhesh2263/chaos-testing/blob/main/assets/system-online.png?raw=true)


## Future work