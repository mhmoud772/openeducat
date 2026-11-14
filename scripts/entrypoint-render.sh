#!/bin/bash
set -e

# Render and cloud platforms supply $PORT for HTTP traffic (e.g. 10000)
HTTP_PORT="${PORT:-8069}"

# If database host/credentials are supplied by Render PostgreSQL
DB_HOST="${HOST:-db}"
DB_USER="${USER:-odoo}"
DB_PASSWORD="${PASSWORD:-odoo123}"
DB_PORT="${DB_PORT:-5432}"

echo "=========================================================="
echo " 🚀 Starting SmartEdu OpenEduCat 19 (Render/Cloud)"
echo " 🌐 HTTP Port: $HTTP_PORT"
echo " 🗄️ Database Host: $DB_HOST (Port: $DB_PORT)"
echo "=========================================================="

# Temporarily unset PORT so Odoo entrypoint doesn't confuse it with postgres port
unset PORT

# Export variables for Odoo official entrypoint
export HOST="$DB_HOST"
export USER="$DB_USER"
export PASSWORD="$DB_PASSWORD"
export PGPORT="$DB_PORT"

exec /entrypoint.sh odoo --http-port="$HTTP_PORT" "$@"
