#!/bin/bash

# Set your node and app labels
NODE_NAME="optiPlex-3070"
APP_LABEL_GATEWAY="app=gateway"
APP_LABEL_UI="app=ui"

echo "=== Chaos Test Started ==="

# 1. Step 1: Drain a node
echo "[1] Draining node: $NODE_NAME"
kubectl drain $NODE_NAME --ignore-daemonsets --delete-emptydir-data
sleep 60

# 2. Step 2: Delete a Gateway pod
GATEWAY_POD=$(kubectl get pods -l $APP_LABEL_GATEWAY -o jsonpath='{.items[0].metadata.name}')
echo "[2] Deleting gateway pod: $GATEWAY_POD"
kubectl delete pod "$GATEWAY_POD"
sleep 30

# 3. Step 3: CrashLoop the Gateway Deployment
echo "[3] Simulating crash loop on Gateway"
kubectl patch deployment gateway -p '{"spec": {"template": {"spec": {"containers": [{"name": "gateway", "command": ["sh", "-c", "exit 1"]}]}}}}'
sleep 60

# 4. Step 4: Delete a UI pod
UI_POD=$(kubectl get pods -l $APP_LABEL_UI -o jsonpath='{.items[0].metadata.name}')
echo "[4] Deleting UI pod: $UI_POD"
kubectl delete pod "$UI_POD"
sleep 30

# 5. Step 5: Scale gateway to 10 replicas
echo "[5] Scaling gateway to 10 replicas"
kubectl scale deployment gateway --replicas=10
sleep 60

# 6. Step 6: Recover Gateway from CrashLoop
echo "[6] Rolling back Gateway deployment"
kubectl rollout undo deployment gateway
sleep 30

# 7. Step 7: Uncordon node
echo "[7] Uncordoning node: $NODE_NAME"
kubectl uncordon $NODE_NAME
sleep 30

# 8. Step 8: Scale gateway down to 2 replicas
echo "[8] Scaling gateway down to 2 replicas"
kubectl scale deployment gateway --replicas=2

echo "=== Chaos Test Completed ==="