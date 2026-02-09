# E2E Tests for Bistro Delivery (Python)

This repository contains end-to-end tests for [Bistro Delivery](https://github.com/hypersequent/bistro), implemented using [Playwright for Python](https://playwright.dev/python/) with pytest.

Prerequisites: Python 3.13+

## Getting Started

1. Clone the repository:

   ```bash
   git clone git@github.com:Hypersequent/bistro-e2e-python.git
   cd bistro-e2e-python
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

4. Install Playwright browsers:

   ```bash
   playwright install --with-deps
   ```

## Running Tests

### Basic Test Execution

```bash
pytest --browser chromium -v    # Run tests in Chromium
pytest --browser chromium -v --headed  # Run tests in headed mode
```

### Upload testing results to QA Sphere

1. Add your QA Sphere credentials to a `.qaspherecli` file or `.env`:

   ```bash
   QAS_TOKEN=<QA Sphere API Token>
   # Get your token in QA Sphere -> Settings -> API Keys

   QAS_URL=<QA Sphere Company URL>
   # Example: https://qasdemo.eu2.qasphere.com
   ```

2. Upload results:

   ```bash
   npx qas-cli junit-upload --project-code BD --attachments junit-results/results.xml
   ```

## Additional Commands

Different browsers:

```bash
pytest --browser chromium -v    # Run tests in Chromium
pytest --browser firefox -v     # Run tests in Firefox
pytest --browser webkit -v      # Run tests in WebKit
```

Linting and formatting:

```bash
ruff check tests/ utils/        # Check for lint errors
ruff format tests/ utils/        # Format code
```

## License

This project is licensed under the 0BSD License - see the [LICENSE](LICENSE) file for details.

---

Maintained by [Hypersequent](https://github.com/Hypersequent)
