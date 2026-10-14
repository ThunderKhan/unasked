# Unasked — M0 model-feasibility probe

**Status: experiment scaffold, not a validated AI model or production backend.** This stage tests whether an existing open-weight model can identify important *unanswered* decisions from notes about **one web-app feature**. It does not build a website, fine-tune a model, or contact real clients.

## Run locally (Windows PowerShell)

From the **repository root**:

```powershell
ollama --version
ollama pull qwen3:4b-instruct
python -m pip install -r evaluation/requirements.txt
python -m pytest evaluation/tests -q
python -m evaluation.probe --model qwen3:4b-instruct
```

If the Ollama background service is not running, start it separately (for example, launch the Ollama application or run `ollama serve` in a different terminal). `ollama ps` can help you check what's loaded. The initial 4B instruct tag is roughly 2.5 GB on disk; runtime memory/latency depends on hardware, available GPU VRAM, model context and other programs. If it proves too slow, **measure and document** an alternative instead of silently substituting one.

The probe calls Ollama locally through the Python client, prints questions and timing, and saves a machine-readable result to `evaluation/results/m0-report.json`. **This results directory should stay out of git**; test only with fictional or anonymized inputs.

Run one case while debugging:

```powershell
python -m evaluation.probe --model qwen3:4b-instruct --case booking
```

## Troubleshooting: the command shows no output or is extremely slow

The first runner version buffered progress until three sequential model requests had completed. This version reports **before and after every call**, uses a default `num_ctx` of 2048, limits generated output to 512 tokens, and sets a **180-second HTTP inactivity timeout** per call (not a guaranteed total execution deadline).

**After checking out the updated branch**, stop any old run with **Ctrl+C**, then check model memory placement:

~~~powershell
ollama ps
nvidia-smi
ollama run qwen3:4b-instruct "Reply with one word: READY"
~~~

The `PROCESSOR` column in `ollama ps` shows GPU, CPU or mixed offload while the model is loaded. If the one-word Ollama test fails or stalls, fix the Ollama/GPU environment first; the Unasked runner is not the cause. Quit unnecessary GPU-heavy apps. If you interrupted a problematic model request, you may free it with `ollama stop qwen3:4b-instruct`.

**Run exactly one M0 inference**, not the full nine-request experiment:

~~~powershell
python -u -m evaluation.probe --model qwen3:4b-instruct --case booking --run unasked_initial
~~~

The output should immediately begin with the model, context budget, and `Starting booking / unasked_initial ...`. If that succeeds, run all three variants for **one case**:

~~~powershell
python -u -m evaluation.probe --model qwen3:4b-instruct --case booking
~~~

Only then run the complete three-case experiment.

If it reports a timeout or `ollama ps` shows mostly CPU and generation is impractically slow, try the smaller **comparison candidate**:

~~~powershell
ollama pull qwen3:1.7b
python -u -m evaluation.probe --model qwen3:1.7b --case booking --run unasked_initial
~~~

Keep the model name and hardware in the report. A smaller model being fast **does not mean it is good enough** at detecting missing requirements. We still need human review.

**Advanced knobs:** `--num-ctx 2048`, `--num-predict 512`, and `--timeout 180` can be set explicitly. Do not arbitrarily make context or output tiny—truncation could cause invalid JSON and false model-quality failures.

## Diagnosing invalid JSON from Gemma

If a single run fails with `Invalid JSON: EOF while parsing a string`, the model may have reached its `num_predict` cap or become repetitive. The runner now includes `diagnostics.done_reason`, `eval_count`, `possible_output_truncation`, and `repetitive_tail_suspected` in its local report. These are **signals**, not a proof of the cause. The report does not store malformed raw model text.

Re-run **one** baseline request using the updated, more concise baseline instruction:

~~~powershell
python -u -m evaluation.probe --model gemma3:4b --case booking --run generic_baseline --output evaluation/results/gemma-baseline-diagnostic.json
~~~

Inspect the metadata:

~~~powershell
$r = Get-Content evaluation/results/gemma-baseline-diagnostic.json -Raw | ConvertFrom-Json
$r.cases[0].results.generic_baseline.diagnostics | Format-List
~~~

If the run is cut off at the output limit but not clearly repeating, a second test may increase `--num-predict 768`. If it is already repeating tokens, **do not solve by blindly increasing the limit**; revise prompts or compare another model.

## Distinguish schema-constrained generation from JSON mode

If **Gemma hits the output limit at both 512 and 768 tokens**, stop increasing `--num-predict`. Repeated tokens or unusual amounts of whitespace may be involved even when the original short tail detector says `false`. The `done_reason=length` field proves **where generation stopped**, not why the model failed to complete the object.

Ollama supports both a strict `format=<JSON Schema>` and a looser `format="json"` mode. The latter is useful as a **diagnostic comparison**; outputs are still passed through the **same Pydantic validation and safety filters**. The probe's default is still schema-constrained mode.

On the known **synthetic** booking case:

~~~powershell
python -u -m evaluation.probe --model gemma3:4b --case booking --run generic_baseline --format-mode json --debug-raw-preview --output evaluation/results/gemma-json-diagnostic.json
~~~

The opt-in `--debug-raw-preview` flag writes the first and last 160 generated characters into the **local ignored report**. Never use it with sensitive or real client notes and don't publish the raw previews. Check whether the model is outputting actual questions, whitespace, repetitions or an unfinished JSON string.

If JSON mode returns a valid meaningful result, the **full complex schema constraint is a likely contributing factor**, and we should simplify that contract and then re-evaluate both models under equivalent conditions. If JSON mode also degenerates, test the model's ability to answer a plain-text question outside the probe (e.g. `ollama run gemma3:4b "For an appointment booking feature, what happens if two visitors choose the same slot? Explain briefly."`) before considering another model.

Do not label the new JSON-mode run directly comparable to earlier **schema-mode** numbers: record `format_mode`, output cap and model with every experiment.

## What the three sample cases do

| Feature | Known missing decision | Already answered in notes | Follow-up decision used for retest |
| --- | --- | --- | --- |
| Booking | Double-booking policy | Cancellation not permitted | Only one confirmed booking per slot |
| Registration | Password recovery | Email verification required | Password-reset link by email |
| Checkout | Failed payment behavior | Create order after successful payment | Keep cart and allow retry |

`cases.json` stores **author-written seed labels, not independently verified gold standards**. It also includes a second open issue in each case. After these smoke cases work, move to the 10 human-reviewed synthetic cases described in `docs/mvp.md`.

## How to decide whether M0 passes

1. **Technical validity:** Every call returns valid schema-constrained JSON, 0–3 questions, and a real model answer (not a canned response). Local tests pass.
2. **Relevance (human review):** For each feature, the suggested questions are truly unanswered, actionable and important. Match meaning, not exact phrasing. The console does **not** calculate or claim these ratings automatically.
3. **No invented evidence:** `removed.fabricated_excerpts` should be empty for the reviewed cases. The filter strips invalid excerpts, but a model that repeatedly invents them still fails the quality goal.
4. **No re-asking:** A resolved decision must not be suggested again, including under different wording or an inconsistent `gap_key`. The code prevents exact-key duplicates; **semantic equivalents require human review** and a better normalization strategy if failures appear.
5. **Measured speed:** Review first and repeated response times on your actual machine. Don't invent a latency threshold before observing them.
6. **Baseline comparison:** Compare `generic_baseline` with `unasked_initial` on the *same notes and model*. Both use the same output schema; Unasked's difference is the reasoning instructions and decision-history handling. If no material difference appears, reconsider differentiation before building UI.

We do **not** claim success, real user value, or willingness to pay from three seed cases. M0's result is a recorded **go / revise / stop** decision.

## Known limitations

- Output uses a model-generated `gap_key`; the deterministic filter catches the same exact key, **not arbitrary paraphrases** with new keys.
- Schema-valid results may still be irrelevant, redundant, factually wrong, or incomplete. Human evaluation is mandatory.
- Prompt-injection resistance is not guaranteed by a system prompt; do not paste production client secrets.
- Scripts deliberately don't auto-modify the planning documents or mark M0 complete.
- This is a **local feasibility tool**, not a deployed public demo.

## Verified sources

- [Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs)
- [Ollama Qwen3 model tags](https://ollama.com/library/qwen3/tags)
- [Pydantic JSON parsing](https://docs.pydantic.dev/latest/concepts/json/)
