# Free-First Resource Catalogue

This catalogue prioritises tools that can be used at $0 without a required subscription. “Free” does not mean unlimited compute, zero setup effort, or permission to use every model/data source commercially. Check current terms before adopting a resource.

## Core tools for all three projects

| Need | Resource | Cost approach | Guardrail |
|---|---|---|---|
| Version control, issues, project docs | [GitHub](https://github.com/) | Public repositories and basic collaboration are free | Keep secrets, private datasets, and credentials out of public repos |
| Automated checks | [GitHub Actions](https://docs.github.com/en/actions) | Standard runners are free for public repositories; private-repo quotas/charges differ | Avoid large model downloads and GPU jobs in CI; monitor usage |
| Python tests | [pytest](https://docs.pytest.org/) | Open source, local | Test software behaviour, not real-world robot safety |
| Linting and formatting | [Ruff](https://docs.astral.sh/ruff/) | Open source, local | Pin versions for repeatability |
| Dependency vulnerability checks | [pip-audit](https://github.com/pypa/pip-audit) | Open source, local/CI | Review findings; don't automatically upgrade blindly |
| Python dependency and project metadata | [pip](https://pip.pypa.io/) and [pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | Free | Pin or constrain dependencies and document tested versions |
| Local model runtime | [Ollama](https://ollama.com/) | Local inference can run without a cloud API subscription | Model downloads use disk/RAM; cloud features/credits are separate |
| Open model discovery | [Hugging Face Models](https://huggingface.co/models) | Many models are downloadable for free | Check each model's licence, commercial terms, safety, and hardware needs |
| Website and performance audit | [Google Lighthouse](https://developer.chrome.com/docs/lighthouse/overview) | Free in Chrome/CLI | Audit is not a guarantee of ranking or conversion |
| Search performance for your own site | [Google Search Console](https://search.google.com/search-console/about) | Free | Requires site ownership verification; results take time |
| Public demo / project documentation | [GitHub Pages](https://pages.github.com/) | Free for eligible public-project use | Check GitHub Pages terms; not a backend for a production AI service |
| Optional one-off site audit | [FreeScan.app](https://www.freescan.app/) | A free audit is currently offered; not required | Paid Pro monitoring exists; use Lighthouse first and do not pay |
| Product/customer research | [GitHub Issues](https://docs.github.com/en/issues) and a simple spreadsheet | Free-first | Record only necessary information; get permission before collecting private data |

## Local AI models: cautious starting point

- Use [Ollama's model library](https://ollama.com/library) or [Hugging Face](https://huggingface.co/models) to find small models.
- Given a laptop with an RTX 3050 4 GB VRAM and memory constraints, start with a small quantized model (roughly 1B–3B parameters) only if local memory and disk space allow. CPU fallback may be slow.
- Do not download several models at once. Check model size and licence first.
- A local language model can help draft documentation, explain logs, generate test ideas, and summarise non-sensitive results. It does not replace deterministic tests, code review, scientific validation, or human approval.
- Never send secrets, confidential customer information, identifiable incident data, or sensitive screening records to a cloud model without explicit authorisation and a suitable data agreement.

## Project-specific guardrails

### Coconut Harvest AI
Use local Python tests and small, reproducible image experiments. Track dataset source, licence, hash, annotation review, split assignment, and test metrics. Treat 0–30 m as a design challenge, not verified robot reach. Do not claim field performance until measured on a suitable, documented test set.

### Extreme Flood Rescue AI
Prefer local simulation and deterministic scenario tests. Clearly label simulated results. Water depths of 1–6 m are scenario targets, not verified operating limits. Never describe the concept as operationally rescue-ready without independent safety and field validation.

### Multimodal Narcotics Screening AI
Use synthetic or explicitly authorised test data. Document reference methods, false positives/negatives, uncertainty, and abstention. A model confidence score or ordinary image alone does not establish chemical identity. Keep a qualified human reviewer in the loop.

## Marketing and sales: start without paid automation

1. Improve the project's own README and public project page before paying for marketing tools.
2. Use Lighthouse for page quality and Search Console to monitor search visibility after the site is indexed.
3. Publish only licensed/authorised images and clearly labelled concept visuals.
4. Make one honest demo and a concise “current status / limitations / next step” section.
5. Contact a small number of relevant growers, engineering partners, or qualified reviewers with a personalised message. Avoid scraped contact lists and bulk unsolicited messages.
6. Do not connect ad accounts, email automation, paid APIs, or subscription tools without explicit approval.

## Free-first policy

- Prefer local tools, public repositories, and reproducible tests.
- No paid API, cloud GPU, subscription, ad spend, or automatic account connection without explicit approval.
- Recheck pricing and licences at the time of use; free tiers and model terms can change.
- Keep a record of each adopted tool, version, purpose, licence, and any usage limit.


## Resource activity check — 26 October 2026

The shared core links were spot-checked and responded: GitHub Actions documentation, pytest, Ruff, pip-audit, Ollama, Hugging Face Models, Lighthouse, and Google Search Console. This checks that pages respond; it does not guarantee future uptime, every feature, or unchanged quotas.

**FreeScan.app is optional, not core.** It currently presents a free one-off audit but also offers paid Pro monitoring. Do not pay for it; Lighthouse is the default. If the free audit disappears, the URL stops responding, or a usable $0 option is no longer available, remove its recommendation and website link.

**Maintenance rule:** remove resources from the catalogue and website when they become unavailable, inactive, or require payment for the useful function. Record the date and reason in the next update and prefer a local/open alternative. Do not delete project code or evidence just because an external service retires. This is a spot-check, not continuous monitoring.

## Automatic no-paid-upgrade policy

- Keep the catalogue limited to tools and services that do not require a paid upgrade for the documented use case.
- The weekly GitHub Actions audit checks curated resource-table URLs for repeated outages and explicit paid-upgrade wording (for example, paid/pro/premium plans or buying credits).
- A table row is removed after three consecutive checks of an explicit paid-upgrade signal or a failed URL. Inconclusive fetches do not count as evidence.
- The scan is a conservative text check, not a guarantee: pricing may be JavaScript-rendered or worded differently. Review the generated audit report; do not treat absence of a flag as proof that a tool is free.
- The automation only removes curated Markdown resource-table rows. It never deletes source code, tests, datasets, evidence, workflows, repository history, or the service account itself.
- No purchase, subscription, billing activation, or paid API call is made. Local/open-source alternatives are preferred.
