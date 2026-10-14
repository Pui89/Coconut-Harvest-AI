# Free-First Setup and Licence Checklist

This guide keeps the Coconut Harvest AI prototype accessible without paid APIs, paid datasets, or required cloud compute. It does **not** promise that every optional model or third-party hosted service will always be free.

## 1. Start with the smallest local workflow

1. Install Python 3.10 or newer and Git from their official websites.
2. Clone this repository.
3. Create a virtual environment so project packages do not affect other Python projects.
4. Install only the dependencies for the demo or test you want to run. Avoid installing the full research/robotics stack unless you need it.
5. Run the lightweight demo and tests before downloading any model checkpoints.

From the repository root:

```bash
git clone https://github.com/Pui89/Coconut-Harvest-AI.git
cd Coconut-Harvest-AI
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

For the current prototype's Python package and test dependencies, see `pyproject.toml` and `requirements.txt`. The repository's Streamlit demo has its own setup instructions in [the demo README](../apps/pui89_app/README.md). Install the smallest relevant dependency set rather than every optional component.

## 2. Free/open-source tools

| Need | Free-first option | Important note |
| --- | --- | --- |
| Source control and code hosting | Git + GitHub Free | Private repository and automation features may have plan limits. |
| Programming | Python | Use a supported version compatible with the project dependencies. |
| Image processing | OpenCV | Open-source software; review third-party component notices if redistributing a packaged application. |
| Model development | PyTorch | Free/open-source framework; model weights have their own licences. |
| Notebooks | Jupyter | Runs locally without a hosted notebook subscription. |
| Tests and formatting | pytest, Ruff | Development tools; install only when needed. |
| Optional hosted notebook | A provider's free tier, if available | Quotas, availability, terms, and billing policies can change. Local CPU experiments remain the no-cloud option. |
| Images | Your own photos or individually verified open-licence images | A public web page or search result does not automatically grant reuse rights. |

No paid API, Roboflow, paid dataset subscription, cloud GPU, or commercial robot simulator is required for the basic local prototype.

## 3. Image and dataset permissions

Before adding each image to the repository or dataset:

- Record the exact source URL, creator/photographer, licence name and licence URL.
- Confirm that the licence covers your intended reuse and redistribution, including whether attribution is required.
- Keep attribution in a dataset manifest or nearby documentation.
- Prefer photographs you took yourself, with appropriate permission for people and private property visible in them.
- Do not use images merely because they are searchable, downloadable, or labelled “free” by a third-party site.
- Do not commit personal data, private images, or images whose licence is unclear.

A suggested manifest format is:

```csv
filename,source_url,creator,license,license_url,notes
example.jpg,https://example.org/image,Creator Name,CC BY 4.0,https://creativecommons.org/licenses/by/4.0/,Replace with verified details
```

The example row is a template only, not a real image attribution.

## 4. Model and software licence checks

- The project's MIT licence applies to this repository's code as stated in [LICENSE](../LICENSE); it does not automatically relicense external models, datasets, or software.
- Before using an Ultralytics/YOLO package or checkpoint, read the current licence for the exact version and intended use. Some use cases may require a separate commercial licence; do not assume all uses are covered by an open-source licence.
- Hugging Face model cards, checkpoints, model code, and required runtimes may have different conditions. Read the model's own licence and hardware requirements.
- Large models may require substantial disk space, RAM, and a capable GPU. A downloadable model is not necessarily practical to run for free.
- Avoid committing model weights to Git. Store large files outside the repository unless there is a clear, permitted reason to include them.

## 5. Prevent surprise bills

1. Prefer local CPU execution for basic development and testing.
2. If you choose a hosted service, check its current free-tier limits and billing settings first.
3. Do not enable paid upgrades, paid API keys, cloud GPU instances, or metered storage unless you intentionally accept the cost.
4. Never put API keys or passwords in source code, notebooks, screenshots, or Git history.
5. Check usage before starting long-running jobs; stop hosted compute when you finish.
6. Remember that this repository cannot control changes to third-party pricing, quotas, account policies, or availability.

## 6. Keep research claims evidence-based

The current demo is a prototype. Displaying an orchard image or producing an illustrative decision report is not proof of trained coconut detection, validated ripeness estimation, physical robot control, or successful autonomous harvesting.

For each experiment, record:

- dataset source and licence;
- number of images and annotation method;
- train/validation/test split and prevention of near-duplicate leakage;
- model name, version, configuration, and random seed where applicable;
- metrics actually measured, such as precision, recall, mAP, inference time, and failure examples;
- hardware and software environment;
- limitations and cases where the system should abstain or request human review.

Do not publish estimated or placeholder metrics as experimental results. If no experiment has been run, label it “planned” or “not yet measured.”

## 7. Practical order of work

1. Confirm the local demo and existing tests run.
2. Collect a small, legally reusable set of representative orchard images.
3. Annotate a modest pilot dataset and document the annotation rules.
4. Run one reproducible baseline experiment with a model whose licence and resource requirements are acceptable.
5. Save predictions, a results CSV, failure examples, and exact commands.
6. Only then consider optional depth sensors, large multimodal models, simulation platforms, or physical robotics.

**Research and safety boundary:** use recorded images and simulation first. Do not connect this prototype directly to physical cutters, motors, or a harvesting arm. Any hardware trial needs independent safety engineering, supervision, and validation.
