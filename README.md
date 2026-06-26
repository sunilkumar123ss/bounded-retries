# Bounded retries for tool adapters

Runnable educational demo/starter with synthetic examples.

Retries only explicitly transient failures, with capped exponential backoff, a maximum attempt count, and a total scheduled-delay budget. Permanent errors stop immediately. The default simulation records proposed delays and does not sleep or call a service. This is not a wall-clock execution timeout: a real adapter also needs per-call timeout/cancellation and idempotency protection for side effects.

## Run

Python 3.10+; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

No network requests, credentials, or paid services are used. Any model/provider integration would be a separate adapter. Read `main.py` for the public functions and `test_main.py` for success/failure invariants. Fixture content is synthetic.

## Scope

This is an educational implementation with synthetic fixtures. Run the tests and inspect the documented limits before adapting it.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
