#!/bin/bash
set -e

# Render sets $PORT for web traffic (e.g. 10000)
HTTP_PORT="${PORT:-8069}"

# If DATABASE_URL is provided by Render (Internal Database URL), parse it
if [ -n "$DATABASE_URL" ]; then
    echo "🔍 Parsing DATABASE_URL from Render environment..."
    eval $(python3 -c "
import os, urllib.parse
url = os.environ.get('DATABASE_URL', '')
if url:
    if url.startswith('postgres://'):
        url = 'postgresql://' + url[11:]
    u = urllib.parse.urlparse(url)
    print(f'PARSED_HOST=\"{u.hostname or \"\"}\"')
    print(f'PARSED_USER=\"{u.username or \"\"}\"')
    print(f'PARSED_PASS=\"{u.password or \"\"}\"')
    print(f'PARSED_PORT=\"{u.port or 5432}\"')
    print(f'PARSED_DB=\"{u.path.lstrip(\"/\")}\"')
")
    DB_HOST="${PARSED_HOST:-$HOST}"
    DB_USER="${PARSED_USER:-$USER}"
    DB_PASSWORD="${PARSED_PASS:-$PASSWORD}"
    DB_PORT="${PARSED_PORT:-5432}"
    DB_NAME="${PARSED_DB:-openeducat}"
else
    DB_HOST="${HOST:-db}"
    DB_USER="${USER:-odoo}"
    DB_PASSWORD="${PASSWORD:-odoo123}"
    DB_PORT="${DB_PORT:-5432}"
    DB_NAME="${DB_NAME:-openeducat}"
fi

echo "=========================================================="
echo " 🚀 Starting SmartEdu OpenEduCat 19 (Render/Cloud)"
echo " 🌐 Web HTTP Port: $HTTP_PORT"
echo " 🗄️ Database Host: $DB_HOST (Port: $DB_PORT)"
echo " 👤 Database User: $DB_USER"
echo " 📁 Database Name: $DB_NAME"
echo "=========================================================="

# Auto-initialize database if empty
echo "🔍 Checking database initialization status..."
TABLE_EXISTS=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d "$DB_NAME" -t -A -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name='ir_module_module';" 2>/dev/null || echo "0")

if [ "$TABLE_EXISTS" != "1" ]; then
    echo "⚡ Database '$DB_NAME' is not initialized!"
    DUMP_FILE="/mnt/extra-addons/openeducat/scripts/init_db.sql.gz"
    if [ -f "$DUMP_FILE" ]; then
        echo "📦 Found pre-built initialized database dump ($DUMP_FILE)!"
        echo "⏳ Restoring SmartEdu OpenEduCat database with Yemen localization..."
        gunzip -c "$DUMP_FILE" | PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -p "$DB_PORT" -d "$DB_NAME" -q || true
        echo "✅ Database restored successfully!"
    fi
else
    echo "✅ Database '$DB_NAME' is already initialized with all modules!"
fi

# Temporarily unset PORT so Odoo entrypoint doesn't confuse it with postgres port
unset PORT

# Export variables for Odoo official entrypoint
export HOST="$DB_HOST"
export USER="$DB_USER"
export PASSWORD="$DB_PASSWORD"
export PGPORT="$DB_PORT"

# Filter out 'odoo' from arguments so it is not passed twice
ARGS=()
for arg in "$@"; do
    if [ "$arg" != "odoo" ]; then
        ARGS+=("$arg")
    fi
done

exec /entrypoint.sh odoo -d "$DB_NAME" --http-port="$HTTP_PORT" "${ARGS[@]}"
