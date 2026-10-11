# AI-Powered Parallel Testing and Debugging Assistant

A beginner-friendly testing harness that compiles and runs a small suite of C programs, executes independent tests concurrently, checks expected results, writes JSON/CSV reports, and optionally asks an LLM to summarize test failures.

> Scope: this is a compiler testing/verification harness, not a compiler implementation. The included test cases are educational examples, not a comprehensive C conformance suite.

## Features

- Automated C compilation with GCC (or another compatible compiler selected through `C_COMPILER`)
- Expected-output and exit-code checking
- A test for expected compilation failure
- Parallel test orchestration with a configurable worker count
- Per-test timeouts
- JSON and CSV reports
- Optional LLM-based failure explanation through an OpenAI-compatible chat-completions endpoint
- GitHub Actions workflow that runs the tests on pushes and pull requests

## Project structure

```text
.
├── .github/workflows/tests.yml
├── cases/
│   ├── manifest.json
│   ├── addition.c
│   ├── function_call.c
│   ├── invalid_syntax.c
│   ├── loop_sum.c
│   └── operator_precedence.c
├── results/
├── runner.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.11+
- GCC available on `PATH`
- Git (for version control)
- `requests` only for the optional LLM integration

## Run locally

Install the optional dependency:

```bash
python -m pip install -r requirements.txt
```

Run the test suite:

```bash
python runner.py
```

Set the worker count:

```bash
python runner.py --workers 1
python runner.py --workers 4
```

Set a timeout per compile/run operation:

```bash
python runner.py --workers 4 --timeout 3
```

The command returns exit code `1` if any test fails. Reports are created at `results/report.json` and `results/report.csv`. These generated reports are ignored by Git so that local results do not accidentally overwrite committed files.

## Enable optional LLM analysis

The LLM is called only when `--ai` is supplied and at least one test failed. Configure environment variables in your terminal; never hard-code or commit your API key.

PowerShell:

```powershell
$env:LLM_API_KEY="your_api_key_here"
$env:LLM_BASE_URL="https://api.openai.com/v1"
$env:LLM_MODEL="gpt-4o-mini"
python runner.py --ai
```

macOS/Linux:

```bash
export LLM_API_KEY="your_api_key_here"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o-mini"
python runner.py --ai
```

Use a model and endpoint supported by your provider/account. The default values are examples; change `LLM_BASE_URL` and `LLM_MODEL` if your provider differs. API usage may incur charges. Test logs are sent to the configured provider when AI analysis is enabled; do not send secrets, private code, or confidential logs.

If the key is missing, tests still run and AI analysis is skipped. LLM output is advisory and may be wrong; verify suggestions yourself.

## How parallel execution works

`ThreadPoolExecutor` schedules independent test jobs concurrently. Each job launches its own compiler and test executable in a separate temporary directory. This is useful for overlapping external compile/run processes. It is not a benchmark proving that every workload becomes faster with more workers; measure timings on your machine before making performance claims.

## Add a test

1. Add a `.c` file under `cases/`.
2. Add an entry to `cases/manifest.json`, for example:

```json
{
  "name": "my_test",
  "source": "my_test.c",
  "expected_stdout": "42",
  "should_compile": true,
  "expected_returncode": 0
}
```

For a test that should fail compilation, set `"should_compile": false`.

## Limitations and safety

- Run only test programs you trust. A timeout limits duration but is not a complete security sandbox.
- Do not use this as a service for arbitrary public C code without stronger isolation, resource limits, and security review.
- The sample suite is small and does not prove compiler correctness.
- The LLM provides debugging hypotheses, not verified diagnoses.
- No API key is required for ordinary tests or GitHub Actions.

## Future improvements

- Add randomized and boundary-value test generation.
- Compare GCC and Clang outputs for selected programs.
- Add structured failure categories and test coverage.
- Produce a sequential-versus-parallel benchmark table.
- Add stronger sandboxing for executing untrusted programs.

## Author

Samyuktha Sri

## License

Choose and add a license if you want others to reuse the project.
