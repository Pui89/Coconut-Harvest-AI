# Cost Safety, Billing and External-Service Policy

**Purpose:** keep this repository local-first and avoid requiring paid services for its basic demos and tests.

## Defaults
- Local execution, synthetic/recorded-data tests, and local simulation are the default.
- Do not automatically provision cloud GPUs, cloud infrastructure, hosted robots, managed databases, paid AI APIs, or paid telemetry services.
- Any paid or remote service must be optional, disabled by default, and documented with pricing, rate limits, privacy implications, and a local alternative.
- Do not commit API keys, tokens, cloud credentials, payment details, environment files, or sensitive sensor/case data.
- Model weights, datasets, simulators, and hosted endpoints can have separate licences, download/storage costs, quotas, and fees. Check the exact provider terms before use.

## Project-specific note
This is a simulation-first coconut-harvesting research prototype. Keep Gazebo/Isaac and model assets local unless you deliberately choose otherwise.
Large model weights and simulation assets may use significant disk space, bandwidth, and GPU resources. Do not auto-download them in installation or CI.

## Before running or merging code
1. Inspect source code, notebooks, dependency manifests, Docker/Compose files, ROS launch files, and GitHub Actions workflows for remote endpoints, cloud provisioning, paid APIs, telemetry uploads, auto-downloads, and unbounded retry loops.
2. Keep remote integrations off unless deliberately configured. Missing credentials should disable an optional integration or fail clearly; code must not create resources or accounts automatically.
3. Review data leaving the machine, model licences, download sizes, and any provider's current pricing.
4. For CI, prefer bounded unit tests and linting; do not run paid inference, rent GPUs, deploy cloud resources, or connect to physical hardware automatically.
5. Use least-privilege workflow permissions, sensible timeouts, and reviewed third-party actions.

## GitHub and provider billing checklist
- Review GitHub Billing & Licensing, usage, Actions, Codespaces, Packages, and any metered features in account/organization settings.
- Disable unused features/workflows. Set budgets and alerts where offered, and verify whether they stop usage or only send notifications.
- Check every separate cloud/AI provider billing dashboard. GitHub settings cannot enforce another provider's spending limits.
- Review past invoices and usage records. Review invoices and usage records directly in the relevant account dashboard.
- For a suspected incorrect charge, contact the provider's official billing support promptly with invoice references and usage dates.

## Local-first operation
Follow the repository's local installation and test instructions. Inspect dependencies before installing. Avoid live-stream, cloud, or hosted-model features unless you intentionally configure them.

## Change-control rule
Any change adding an external endpoint, API key, cloud resource, auto-download, telemetry export, or paid service must update this file and explain the service, default state, data leaving the machine, cost limits/disable steps, licence/pricing, and local alternative.

## Zero-cost local mode (default)

Treat this repository as **local-only and no-paid-services-by-default**. This is a development policy, not a technical guarantee that external providers cannot bill an account.

- Do not add API keys, payment methods, paid endpoints, cloud deployments, cloud GPUs, managed databases, paid telemetry, or paid CI as a requirement for the core demo.
- Do not create cloud resources, subscribe to services, or start remote jobs automatically. No missing credential should trigger account creation or a paid fallback.
- Keep remote inference, data uploads, live streams, robot hardware, and telemetry disabled unless a maintainer deliberately enables them after reviewing cost, privacy, and safety.
- Prefer small local models and optional model downloads. Do not automatically download large model weights or datasets during installation or tests. Show download size and license before a user chooses to fetch them.
- Run tests against synthetic fixtures by default. Tests and CI must not call external paid APIs, upload sensor data, deploy infrastructure, or command physical actuators.
- Before any optional external service is used, require a deliberate configuration change and document: provider, pricing/quota, data sent, credential setup, shutdown/removal steps, and a free local alternative.
- Keep secrets out of Git. Use environment variables or a local ignored configuration file; provide a safe example file containing placeholders only.
- Use finite timeouts, bounded retries, download-size limits where feasible, and explicit error messages. Never retry billable remote calls indefinitely.
- Keep an independent local clone and backups of source code, documentation, and irreplaceable data. Public hosting, model availability, and third-party policies can change.

### Safe operating checklist

1. Work from a local Git clone and create a virtual environment.
2. Read dependency manifests before installing; avoid commands that install optional heavy extras unless needed.
3. Run the documented synthetic demo and unit tests first.
4. Inspect workflows and scripts before enabling cloud, remote model, streaming, telemetry, or hardware features.
5. Check GitHub billing/usage and each provider's billing page separately. Alerts may notify without stopping usage; do not assume a budget is a hard spending cap.
6. If you want a strict no-charge approach, do not configure payment methods or enable any service that requires billing. Review account usage directly in the relevant account dashboard.

**Project-specific zero-cost note:** Coconut-specific rule: no automatic downloads of large vision models, datasets, or simulation assets; use synthetic/local orchard samples by default.


## Hosted CI is opt-in

To reduce surprise usage, repository workflows are configured for manual `workflow_dispatch` runs rather than automatic push, pull-request, or scheduled runs. This prevents routine commits from automatically starting hosted jobs, but it does **not** make a manually launched job free or disable GitHub Actions at the account level.

For a strict $0 operating target:
- Do not click **Run workflow** and do not enable hosted deployments, cloud jobs, or external integrations.
- Run tests and demos locally on your own computer.
- Before enabling any workflow, review its runner time, artifact uploads, external services, and your current GitHub plan/usage.
- Keep deployments and physical robot/actuator paths disabled unless you deliberately review and approve them.


## No third-party online service required

The supported default workflow is local development, local tests, synthetic examples, and local simulation. The project does not require a paid cloud API, hosted AI inference, cloud GPU, managed database, or telemetry vendor to run its basic demos and tests. Optional model weights and optional hardware integrations are separate opt-ins, not prerequisites.

- Do not configure API keys, cloud credentials, remote inference endpoints, hosted databases, or telemetry brokers for the default workflow.
- Model weights are cache-only by default where the project provides the guarded loader. Do not set `PUI89_ALLOW_MODEL_DOWNLOAD=1` unless you intentionally approve a large download and its license/storage/network requirements.
- Use local files rather than third-party URLs for evidence inputs.
- Keep hosted CI, website deployment, and other hosted workflows off unless you intentionally choose to use them and have checked the account's usage limits.
- Open-source Python packages may still need to be downloaded during initial installation. That is not the same as subscribing to a paid online service; use a local package cache or pre-downloaded wheels if you need installation without network access.

For a strict zero-spend setup, use the project locally and keep all hosted features disabled.
