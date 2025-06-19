#!/bin/bash
NAMESPACE="default"
LABEL="app=gateway"

echo "[*] Killing all Gateway pods..."
kubectl delete pods -l $LABEL -n $NAMESPACE

echo "[*] Waiting for recovery..."
sleep 15
kubectl get pods -l $LABEL -n $NAMESPACE