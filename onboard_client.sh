#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# onboard_client.sh
# Automates the full setup for a new client company.
# Usage: ./scripts/onboard_client.sh --name client_id
# ─────────────────────────────────────────────────────────────────

set -e

CLIENT_ID=""
KNOWLEDGE_DIR=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --name) CLIENT_ID="$2"; shift ;;
        --knowledge) KNOWLEDGE_DIR="$2"; shift ;;
    esac
    shift
done

if [ -z "$CLIENT_ID" ]; then
    echo "Error: --name is required"
    exit 1
fi

echo "Onboarding client: $CLIENT_ID"

# 1. Create client directory from template
echo "[1/5] Creating client directory..."
cp -r ./client_template "./clients/$CLIENT_ID"
echo "  Done. Edit ./clients/$CLIENT_ID/config/client.yml before continuing."
echo "  Press ENTER when ready..."
read

# 2. Ingest knowledge documents
if [ -n "$KNOWLEDGE_DIR" ]; then
    echo "[2/5] Ingesting knowledge documents..."
    ./scripts/ingest_knowledge.sh --client "$CLIENT_ID" --source "$KNOWLEDGE_DIR"
else
    echo "[2/5] Skipping knowledge ingestion (no --knowledge path provided)"
fi

# 3. Setup NemoClaw sandbox
echo "[3/5] Setting up NemoClaw sandbox..."
nemoclaw onboard --name "client_$CLIENT_ID" --network-policy restricted

# 4. Create Kubernetes namespace
echo "[4/5] Creating Kubernetes namespace..."
sed "s/CLIENT_ID/$CLIENT_ID/g" ./infra/kubernetes/client-template/deployment.yml     | kubectl apply -f -

# 5. Health check
echo "[5/5] Running health check..."
./scripts/health_check.sh --client "$CLIENT_ID"

echo ""
echo "Client $CLIENT_ID is ready."
