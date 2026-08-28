# Example Benchmark Submission

This directory demonstrates the expected structure for a benchmark submission to the Open LLM Benchmark Database (OLBD).

Replace the example files with your own benchmark results and hardware evidence while preserving the expected directory structure and filenames.

## Required Files

Every submission must include the following hardware evidence files:

```text
cpu.txt
memory.txt
system.txt
windows.txt
nvidia-smi.txt
```

Benchmark run files use the following naming convention:

```text
benchmark-v0.9-p512-run1.txt
benchmark-v0.9-p512-run2.txt
benchmark-v0.9-p512-run3.txt
```

Three benchmark runs are required by the current OLBD Benchmark Protocol. Historical two-run submissions may still be recognized and clearly labeled as legacy results.

## Submission Manifest

New submissions should include:

```text
submission.json
```

The manifest contains submission-level metadata used by the parser.

Example:

```json
{
  "schema_version": "1.0",
  "submission_name": "Example_GPU_Submission",
  "submitted_at": "2026-08-15T00:00:00Z",
  "benchmark_timestamp": "2026-08-15T00:00:00Z"
}
```

Fields:

- `schema_version` identifies the submission manifest schema.
- `submission_name` provides a human-readable identifier for the submission.
- `submitted_at` records when the submission package was submitted.
- `benchmark_timestamp` records when the benchmark was performed.

Timestamps must use ISO-8601 format.

Historical submissions without `submission.json` remain supported through the legacy folder-based submission workflow.

## Evidence and Results

Hardware identity is determined from the preserved hardware evidence files.

Benchmark measurements are determined from the preserved raw benchmark output files.

The submission manifest does not replace or override these authoritative source files.

## Example Data Note

The benchmark files currently included in this example directory are a preserved historical two-run result.

Because the current OLBD Benchmark Protocol requires three runs for new submissions, validating this example will produce a warning that only two benchmark run files are present. This is expected and demonstrates backward compatibility with legacy submissions.

Do not create or modify benchmark output solely to eliminate this warning.

## Validate the Example

From the OpenLLMWorks repository root, run:

```powershell
py -m parser.validate .\example_submission
```

The example should pass structural validation while reporting one warning because it intentionally preserves a historical two-run benchmark result.

Expected validation summary:

```text
[OK] submission.json
[OK] Manifest schema 1.0
[OK] Hardware evidence (5/5 required files present)
[WARN] Benchmark runs (2 found; 3 required for new submissions)

Warnings:
- Fewer than 3 benchmark run files were found (2 present).

Validation PASSED with 1 warning(s).
```

This warning is expected.

It demonstrates that OpenLLMWorks can preserve and recognize legitimate historical submissions while enforcing the current three-run requirement for new benchmark contributions.

A warning does not mean that the preserved historical result should be altered. Raw benchmark evidence should remain unchanged.

## Notes

- Do not edit benchmark output files.
- Preserve raw benchmark output.
- Complete three benchmark runs for new submissions.
- Preserve the required hardware evidence files.
- Include a valid `submission.json` for new submissions.
- Validate the completed submission before contributing it.
- Follow Benchmark Protocol OLBD-BP-1.0.

Additional information can be found in:

```text
docs/benchmark_v1.md
```