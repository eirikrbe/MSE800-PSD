# Kubernetes (minikube) deployment

## Files

- `backend.yaml`     — Deployment + NodePort Service for the FastAPI backend (nodePort 30080)
- `frontend.yaml`    — Deployment + NodePort Service for the React frontend (nodePort 30173)
- `combined-pod.yaml` — A single Pod running both containers + one Service exposing both ports

All Deployments/Pods use `imagePullPolicy: Never` because we load images directly into minikube instead of pulling from a registry.

## Note on the kubectl command

We use `minikube kubectl --` instead of plain `kubectl` — this runs the kubectl bundled with minikube, so you don't need a separate kubectl install. The `--` separates minikube's args from kubectl's.

> Tip: alias it once and you can just type `kubectl ...` for the rest of your shell session:
> ```bash
> alias kubectl="minikube kubectl --"
> ```

---

## Path A — separate frontend + backend manifests

```bash
# 1. Start minikube
minikube start

# 2. Build the images (pick ONE of the two sub-paths)

#    A1. Build directly inside minikube (no host docker needed)
minikube image build -t learning-app-backend:latest  ./backend
minikube image build -t learning-app-frontend:latest ./frontend

#    A2. Or build on host docker, then load into minikube
# docker build -t learning-app-backend:latest  ./backend
# docker build -t learning-app-frontend:latest ./frontend
# minikube image load learning-app-backend:latest
# minikube image load learning-app-frontend:latest

# 3. Apply the manifests
minikube kubectl -- apply -f k8s/backend.yaml
minikube kubectl -- apply -f k8s/frontend.yaml

# 4. Watch pods come up
minikube kubectl -- get pods -w

# 5. Open the services (each command prints/opens a URL)
minikube service frontend
minikube service backend
```

## Path B — single multi-container Pod

```bash
# 1. Start minikube
minikube start

# 2. Build the images (same as Path A — choose one sub-path)
minikube image build -t learning-app-backend:latest  ./backend
minikube image build -t learning-app-frontend:latest ./frontend

# 3. Apply the combined manifest
minikube kubectl -- apply -f k8s/combined-pod.yaml

# 4. Watch it come up
minikube kubectl -- get pod learning-app -w

# 5. Access it (see "Accessing the app" below)
```

---

## Inspect what's running

```bash
minikube kubectl -- get pod,svc
minikube kubectl -- describe pod learning-app
minikube kubectl -- logs learning-app -c backend
minikube kubectl -- logs learning-app -c frontend
minikube kubectl -- exec -it learning-app -c backend -- sh   # note the two `--`
```

## Accessing the app

Because minikube on Linux uses the **docker driver**, NodePorts at `192.168.49.2:<port>` are not reachable from the host browser. Use port-forward instead:

```bash
# Forward both ports from the Pod to your laptop (keep this terminal open)
minikube kubectl -- port-forward pod/learning-app 8000:8000 5000:5000
```

Then open:
- Frontend: http://localhost:5000
- Backend:  http://localhost:8000/api/hello

The frontend's `App.jsx` fetches `http://localhost:8000/api/hello`, which works as long as the backend port-forward is running.

## Quick reference — which CLI does what

| Task                       | Tool     | Command                                  |
|----------------------------|----------|------------------------------------------|
| Start/stop cluster         | minikube | `minikube start` / `minikube stop`       |
| Build image into cluster   | minikube | `minikube image build`                   |
| Load host image into cluster | minikube | `minikube image load`                  |
| List images in cluster     | minikube | `minikube image ls`                      |
| Apply manifest             | kubectl  | `minikube kubectl -- apply -f`           |
| Inspect resources          | kubectl  | `minikube kubectl -- get / describe / logs` |
| Open Service in browser    | minikube | `minikube service <name>`                |
| Port-forward               | kubectl  | `minikube kubectl -- port-forward`       |

---

## How networking works here

There are three "localhosts" in play. Knowing which is which prevents 90% of the confusion.

```
┌──── your laptop ────┐    ┌──── minikube node (a Docker container) ────┐
│                     │    │                                            │
│  browser            │    │  ┌─── Pod: learning-app ──────────┐        │
│    │                │    │  │                                │        │
│    │ http://localhost:5000│  │  frontend container :5000      │        │
│    │ http://localhost:8000│  │  backend  container :8000      │        │
│    ▼                │    │  │  (both share the same          │        │
│  127.0.0.1:5000 ────┼────┼──┼─▶ network namespace, so they   │        │
│  127.0.0.1:8000 ────┼────┼──┼─▶ reach each other on          │        │
│   (kubectl          │    │  │  localhost)                    │        │
│    port-forward)    │    │  └────────────────────────────────┘        │
│                     │    │                                            │
└─────────────────────┘    └────────────────────────────────────────────┘
```

### 1. Browser → laptop port (`localhost:5000`, `localhost:8000`)

When the React app does `fetch('http://localhost:8000/api/hello')`, **the fetch runs in your browser, not inside the container.** So `localhost` here means *your laptop*, not the Pod. That's why we need `kubectl port-forward` — to put something on your laptop's `:8000` for the browser to actually reach.

### 2. Laptop port → Pod port (via `kubectl port-forward`)

`kubectl port-forward pod/learning-app 5000:5000 8000:8000` opens TCP listeners on `127.0.0.1:5000` and `127.0.0.1:8000` on your laptop. Each incoming connection is tunneled through the Kubernetes API server, into the Pod, and onto the matching container port. When the port-forward process dies, those tunnels die too.

> We use port-forward because minikube's **docker driver** on Linux makes NodePorts unreachable from the host browser (the `192.168.49.2` IP only exists inside Docker's internal network).

### 3. Container ↔ container inside the Pod (`localhost`)

Every container in the same Pod shares one network namespace. So *if the backend wanted to call the frontend* (or vice versa) **from inside the cluster**, it could just hit `http://localhost:5000`. No Service needed, no DNS lookup. This is what makes multi-container Pods a useful pattern for sidecars.

### 4. Pod ↔ Pod across the cluster (via Services)

If you had used Path A (separate `backend` and `frontend` Deployments in different Pods), the frontend Pod could not use `localhost` — it would reach the backend through its Service DNS name: `http://backend:8000`. The Service's stable ClusterIP load-balances across whatever Pods match its selector. (Browsers still can't use these names — they only resolve inside the cluster.)

### 5. Service types you'll see

| Type | Reachable from |
|---|---|
| **ClusterIP** | inside the cluster only (Pod-to-Pod traffic, internal APIs) |
| **NodePort** | ClusterIP + each node's IP on a high port (30000–32767) |
| **LoadBalancer** | NodePort + an external cloud load-balancer IP (not applicable to minikube) |

Our `learning-app` Service is `NodePort`, but on the docker driver we ignore the NodePort and use `port-forward` instead — same end result, fewer surprises.

---

## Delete the app

### Step 1 — Stop the port-forwards

They live in the terminal(s) you ran them in. Either:
- Press **Ctrl+C** in each terminal, or
- Kill them all from anywhere:
  ```bash
  pkill -f "kubectl.*port-forward"
  ```

### Step 2 — Delete the Kubernetes resources

```bash
# Path B (combined pod)
minikube kubectl -- delete -f k8s/combined-pod.yaml

# Path A (separate deployments) — if you applied these instead
# minikube kubectl -- delete -f k8s/backend.yaml -f k8s/frontend.yaml
```

Verify nothing is left except the built-in `kubernetes` service:
```bash
minikube kubectl -- get pod,svc
```

### Step 3 — Remove the images

```bash
# From minikube's image store
minikube image rm learning-app-backend:latest learning-app-frontend:latest

# From your host docker (only if you used `docker build` in path A2)
docker rmi -f learning-app-backend:latest learning-app-frontend:latest
```

Verify they're gone:
```bash
minikube image ls | grep learning-app   # should print nothing
docker images       | grep learning-app   # should print nothing
```

### Step 4 — (Optional) Stop or delete the cluster itself

```bash
minikube stop       # pauses the cluster — `minikube start` brings it back fast
# OR
minikube delete     # nukes the cluster entirely (cluster state, images, all gone)
```

Use `stop` if you'll come back to this project soon; `delete` if you're done for a while and want the disk space back.
