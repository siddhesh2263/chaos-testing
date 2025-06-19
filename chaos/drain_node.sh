#!/bin/bash
POD=$(kubectl get pod -l app=db-writer -n default -o jsonpath="{.items[0].metadata.name}")
NODE=$(kubectl get pod $POD -n default -o jsonpath="{.spec.nodeName}")

echo "[*] Draining node $NODE..."
kubectl drain $NODE --ignore-daemonsets --delete-emptydir-data

sleep 20
kubectl get pods -l app=db-writer -n default