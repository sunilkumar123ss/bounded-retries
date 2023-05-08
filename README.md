# Bounded retries for tool adapters

> **Disclosed reconstruction prepared on 24 October 2026.** The recorded Git dates are synthetic, not dates of past development. See [HISTORY.md](HISTORY.md).

This is an incomplete stage in a tutorial reconstruction of an already-completed reference implementation. Source, fixtures, tests, command-line behavior and verification are introduced in later stages. Only the final branch tip contains the complete documented package.

## Intended scope of the final example

Retries only explicitly transient failures, with capped exponential backoff, a maximum attempt count, and a total scheduled-delay budget. Permanent errors stop immediately. The default simulation records proposed delays and does not sleep or call a service. This is not a wall-clock execution timeout: a real adapter also needs per-call timeout/cancellation and idempotency protection for side effects.

All examples are synthetic and educational. This reconstruction does not establish historical employment, deployment, usage, or production benchmarks.
