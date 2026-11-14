FROM odoo:19

USER root

# Install lightweight tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration
COPY ./odoo.conf /etc/odoo/odoo.conf

# Copy extra addons
COPY . /mnt/extra-addons/openeducat

# Copy startup entrypoint
COPY ./scripts/entrypoint-render.sh /entrypoint-render.sh
RUN chmod +x /entrypoint-render.sh

# Fix permissions
RUN chown -R odoo:odoo /mnt/extra-addons/openeducat /etc/odoo/odoo.conf

USER odoo

EXPOSE 8069

ENTRYPOINT ["/entrypoint-render.sh"]
CMD ["odoo"]
