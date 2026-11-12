# Odoo 20 migration status (work in progress)

> This is an **incremental migration branch**, not a working SaaS platform for production.
> It starts from the repository's `12.0` branch; the repository default branch is `11.0`.

## What has actually been ported

- `saas_base`: manifest moved to 20.0, explicit `base` dependency. Existing abstract model and exception classes use ORM constructs still supported by Odoo 20.
- `auth_oauth_check_client_id`: manifest moved to 20.0, override compared with Odoo 20 `auth_oauth.models.res_users.ResUsers._auth_oauth_validate`. Replaced `assert` with `odoo.exceptions.AccessDenied` so failed checks are enforced even with Python optimization.
- The following **legacy, unported** addons were explicitly marked `installable=False` to avoid accidentally deploying old database-management code on Odoo 20: `auth_oauth_ip`, `saas_client`, `saas_server`, `saas_server_backup_ftp`.
- Other addons that were already marked `installable=False` remain disabled. Their `11.0`/`12.0` manifest versions were intentionally not relabeled as migrated.

## Not yet migrated (critical path)

1. **Authentication**: port `auth_oauth_ip` and `oauth_provider` to current Odoo authentication APIs; validate audience / issuer / token provenance independently of the optional `client_id` claim. Review internal-only OAuth endpoints and timeout/SSRF protections.
2. **Client instances**: port `saas_client` and resolve `web_settings_dashboard` / `access_limit_records_number` dependencies. Rewrite obsolete settings and QWeb/JS assets integration.
3. **Server control**: port `saas_server` and database/registry operations (`odoo.service.db`, provisioning, installing addons, backups). Rework public HTTP routes that call `sudo()` for database creation, deletion or management: enforce authentication, authorization, replay protection and tenant isolation before enabling.
4. **Portal**: port `saas_portal`, `saas_utils` and `saas_portal_*` modules; update `@api.multi`, `ir.sequence.get`, old imports, views (`<tree>` -> `<list>`, old `attrs`/`states`, obsolete `view_type`) and scheduled actions to Odoo 20.
5. **Commercial and infrastructure integrations**: validate/replace third-party dependencies `contract`, `product_price_factor`, OCA `connector`, website addons, S3/FTP, DNS, Mailgun, AWS and payment/subscription integration, module by module.
6. **Provisioning script**: `saas.py` still sets `ODOO_VERSION = 11` and calls legacy server / CLI APIs; it must not be used to provision Odoo 20 until rewritten.

## Validation

- The two migrated modules are **source-adapted only**. No Odoo 20 test database is available in this work environment; installation and end-to-end SaaS flows have **not** been verified.
- On a disposable Odoo 20 server with the Odoo and this repo's addons paths configured, install only `saas_base` and `auth_oauth_check_client_id` first, then test login success, client ID mismatch and OAuth response without `client_id`.
- Before enabling any SaaS provisioning module, integration-test creation, synchronization, upgrades, backup/restore, suspension and deletion across portal/server/client databases. Use isolated databases and least-privilege credentials.

## Useful references

- [Odoo 20 manifests](https://www.odoo.com/documentation/20.0/developer/reference/backend/module.html)
- [Odoo 20 source installation](https://www.odoo.com/documentation/20.0/administration/on_premise/source.html)

**Do not deploy this branch as a complete SaaS solution.**
