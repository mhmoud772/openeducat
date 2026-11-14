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
else
    DB_HOST="${HOST:-db}"
    DB_USER="${USER:-odoo}"
    DB_PASSWORD="${PASSWORD:-odoo123}"
    DB_PORT="${DB_PORT:-5432}"
fi

echo "=========================================================="
echo " 🚀 Starting SmartEdu OpenEduCat 19 (Render/Cloud)"
echo " 🌐 Web HTTP Port: $HTTP_PORT"
echo " 🗄️ Database Host: $DB_HOST (Port: $DB_PORT)"
echo " 👤 Database User: $DB_USER"
echo "=========================================================="

# Check if DB_HOST is still defaulting to 'db' on Render
if [ "$DB_HOST" = "db" ] && [ -n "$RENDER" ]; then
    echo "⚠️ [ERROR] Database Host is set to 'db' on Render!"
    echo "⚠️ You must set 'DATABASE_URL' or 'HOST' in your Render Environment settings."
fi

# Temporarily unset PORT so Odoo entrypoint doesn't confuse it with postgres port
unset PORT

# Export variables for Odoo official entrypoint
export HOST="$DB_HOST"
export USER="$DB_USER"
export PASSWORD="$DB_PASSWORD"
export PGPORT="$DB_PORT"

exec /entrypoint.sh odoo --http-port="$HTTP_PORT" "$@"
