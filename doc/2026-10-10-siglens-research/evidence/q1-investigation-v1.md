# Technical Q1: Grok 1.0.52 controlled isolation investigation

- Evidence version: v1, 2026-10-13
- Function: technical-design, overall; Engineering Lead acting as Architect
- Owning issue: [ISSUE-6](mention://issue/01a13437-0660-74e5-a7db-2d2182049029)
- Request: Project Manager comment `01a13450-254e-72f9-93e8-7475f7802792`, under author handoff `01a1344c-0ced-7d79-ba75-a3a41c25ccaf`. Retrieve through `multica issue comment list 01a13437-0660-74e5-a7db-2d2182049029 --thread 01a1344c-0ced-7d79-ba75-a3a41c25ccaf --tail 30 --compact --output json`.
- Design examined: [technical-design.md v1 @ 060643a](https://github.com/patgu9/Siglens/blob/060643a5b3285ecaa811c813bcc4173098c0ee5a/doc/2026-10-10-siglens-research/technical-design.md), especially Q1, C2/C8 and T8; [original evidence](https://github.com/patgu9/Siglens/blob/060643a5b3285ecaa811c813bcc4173098c0ee5a/doc/2026-10-10-siglens-research/evidence/overall-v1.md)
- Product input: approved v10 `9c16ff29cf26d96ea126fbbb09494a91aae613d4`, with the unchanged approval sources recorded in that design and coordination [ISSUE-5](mention://issue/01a133bc-88a1-7b10-80d4-f5f251e72ecf)
- Artifacts: [executable investigation fixture](q1-probe.py), [selected actual observations](q1-results.json)

## Conclusion and scope

**Q1 remains OPEN.** The real installed Grok binary removes the observed local tools under the tested profile and rejects five forced tool calls. However, the same profile does not prevent a configured MCP process from starting. Profile text and an empty main-request tool list are therefore insufficient evidence for process isolation.

An additional macOS executable allowlist stopped that synthetic MCP startup while the fixture request still completed. This establishes a bounded alternative to investigate, not a production sandbox or an approved design change. Authenticated hosted X retrieval was not verified. The custom-model fixture exposes no hosted X tool; that absence cannot establish what the login-backed service supports.

The investigation delivered actual local registry, dispatch, configuration-startup and OS checks. It stops before credentials or real source ingestion because the tested route does not establish the login-backed X boundary. The missing live-test inputs and their suppliers are specified below. No product policy or first-release channel was changed.

## Binary, environment and evidence boundary

| Item | Observed identity or boundary |
| --- | --- |
| Binary | `grok 1.0.52 (0920c8169e27)`, resolved versioned executable, not an updater's symlink |
| SHA-256 | `c2caa9895dd763297a75e8fb6077e175d9c5304c53903e52cff8891a1384bbb9` |
| Host | macOS 27.0.1, build 26A434; Python 3.14.7 |
| Source matching | GitHub's official repository lookup for `0920c8169e27` returned HTTP 422, no matching commit. This investigation does not claim a source-to-binary audit. |
| Comparison material | last30days `grok_x.py` at `50998cd1ba583f13a63b20e3fb5d906c71c31655` remains an input, not evidence that its audited 1.0.46 build covers this binary. |
| Credentials | Fresh `GROK_HOME` for every case; synthetic fixture keys only. No existing login, auth store, keychain, credential environment, refresh token or real research data was read or copied. |
| Network | A loopback HTTP fixture supplies model responses. An outer `sandbox-exec` policy denies network access except that case's loopback port. No xAI/X inference or external publication request was permitted. |
| Files and lifecycle | Outer guard denies reads under `/Users` except the case directory and pinned binary; writes are limited to the case directory and `/dev/null`. Each invocation runs in its own process group, has a 35-second timeout, and is collected/cleaned in the foreground. No background service is handed off. |

The CLI configuration points a custom `q1-fixture` model at the loopback server. The server replaces only upstream responses: it emits a fixed answer or a chosen tool call. The Grok executable, registration, argument handling, tool dispatch and OS enforcement are real. This differs from mocking `subprocess.run` in a unit test, but it still does not reproduce OAuth, the hosted model, X data or all production initialization paths.

The captured primary requests are distinguished from Grok's auxiliary title/dashboard requests. A title request contains a `session_title` function; it is not the main agent's action registry. The selected observations retain the main request path, model, tool names and returned tool messages. Local absolute paths are replaced with `<FIXTURE_ROOT>` and `<PINNED_BINARY>`. Complete generated vendor system prompts are omitted. SHA-256 values identify the original local captures; they are not a substitute for the included observations.

## Actual checks and outcomes

All substantive CLI cases below exited 0. That is only CLI completion; the tool results and side-effect observations establish each stated conclusion.

| Check and case names | Actual observation | What it establishes / does not establish |
| --- | --- | --- |
| Registry control: `baseline-registry` | Main Chat Completions request advertised 24 tools, including read, write, terminal, discovery and integration tools. | Positive control that this fixture observes a real nonempty main registry. `--no-subagents` was common to all cases, so no conclusion about profile-only subagent removal is made. |
| Positive dispatch: `positive-read` | The fixture forced `read_file` with its real `target_file` argument. The next model request contained `1→Q1_SYNTHETIC_READ_SENTINEL`. | Real tool execution works in the control; an empty tool result is not being mistaken for a successful test harness. |
| Profile registry: `registry-profile-2` | Main request advertised no tools. | Local registry removal for this binary/configuration/model path. Auxiliary functions and other authentication paths are separate. |
| Forced forbidden calls: `deny-read`, `deny-shell`, `deny-write`, `deny-search`, `deny-use` | Each main request advertised no tools. Forced `read_file`, `run_terminal_command`, `write`, `search_tool`, and `use_tool` calls returned `Tool not found: <name>`. The synthetic file retained its original bytes. | The five calls reached actual dispatch and failed lookup, rather than merely being omitted from a prompt. This is not a proof against every possible tool or startup action. |
| Configured startup: `context-control`, `context-profile` | A configured MCP command `/usr/bin/touch` created the synthetic `mcp-started` marker in both cases. The profile case still had an empty main registry. | Finding **Q1-F1**: `mcpInheritance: none` in this profile does not prevent this configured process startup. This can precede model tool use. No claim is made about registration by a fully functioning MCP server; the canary intentionally exits without a handshake. |
| Local instructions: the same two context cases | A synthetic AGENTS.md marker was absent from both main requests. | **Inconclusive** for `agentsMd: false`: the control did not demonstrate ingestion, so no profile suppression pass is claimed. Skill discovery and hooks were not tested. |
| OS executable restriction: `context-profile-os-exec` | With process execution restricted to the pinned Grok executable, the MCP marker was absent, main tools remained empty and the fixture request completed. Directly invoking `/usr/bin/touch` through that guard returned exit 71 / Operation not permitted. | The OS restriction blocks this observed startup command. It is an executable allowlist, not a claim that the process cannot fork or re-execute the allowed Grok binary. |
| OS filesystem/socket controls: `os-guard` | Reading an allowed synthetic file and connecting to the allowed loopback listener succeeded. Reading/writing outside the allowed case and connecting to a second live loopback listener failed with Operation not permitted; no forbidden file was created. | Actual macOS enforcement for those paths and sockets. No cross-platform guarantee, DNS/redirect proof, or complete OS escape audit. |
| Hosted-X distinction: `hosted-x-fixture` | With `supports_backend_search = true` and the additional `GROK_BACKEND_SEARCH=true` probe, the custom-model main request still had no tools. Forced local `x_keyword_search` returned Tool not found. | This custom-model/local-dispatch test does not exercise server-hosted X execution. It neither passes an X-only retrieval test nor proves that logged-in X is unavailable. The environment flag's effect on this build is not established. |

The first guard attempt (`registry-profile`) exited 65 because `sandbox-exec` requires `localhost`, not the numeric loopback address in that policy expression. No model request occurred; it supplies no isolation evidence. The subsequent guard used the accepted syntax. An early forced-read case used `file_path`; the final `deny-read` and positive control use the correct `target_file`. Both attempts are retained rather than silently presenting only successful setup.

### Q1-F1: profile is not a process-startup boundary

Location: technical v1 Section 2's reference-isolation assumption, Q1 and C2/C8/T8. The controlled profile sets `injectDefaultTools: false`, `discoverSkills: false`, `agentsMd: false`, `mcpInheritance: none`, declares `GrokBuild:read_file`, then removes read/discovery/use/Agent tools through the CLI. The resulting main registry is empty, yet the seeded MCP command starts.

Consequence: a wrapper that reuses an operator's existing configuration could run configured processes before research tool dispatch. An empty tool list does not justify copying or exposing the normal login/configuration directory. This is a narrower observed behavior than a claim that source text can escape the tested profile. The investigation did not send adversarial real sources or use real credentials.

Disposition: **OPEN**, attached to existing technical Q1. Blocks approval of profile-only X isolation and the dependent X adapter breakdown/coding. It does not contradict the core's typed-unavailable-channel seam or remove X from complete acceptance. No separate product finding is opened.

## Alternatives and next evidence

| Option | Benefit | Cost, current evidence and limit |
| --- | --- | --- |
| Profile alone with ordinary user configuration | Low operational work | Rejected as sufficient isolation evidence by Q1-F1. Keeping the main tool registry empty does not prevent the observed startup. |
| Clean per-run Grok configuration plus OS restrictions | Preserves the Grok-login direction while separating unrelated user files/configuration; an exec allowlist stopped the canary | Candidate, not yet selected. Requires an explicit allowed filesystem/network/IPC boundary and safe credential lifecycle. The tested guard is a safety fixture: it broadly allows other system operations and is not a production policy. Login/refresh behavior, hooks/plugins, allowed-binary re-execution, broader system paths and platform support remain unverified. |
| Dedicated disposable OS account or VM with its own Grok login | Stronger separation from the operator's existing session and a place to permit real X network access | Candidate, not tested here. Adds setup and controlled evidence transfer. An independently authorized login avoids copying or refreshing the existing session. Network egress and source/metric provenance still need validation. |

Recommended next investigation: use an operator-provided disposable environment with a separate authorized Grok login and a pinned build. Before source ingestion, verify the effective startup configuration, actual login-backed request/tool path, permitted X operations, and forbidden local/indirect operations. Then run a bounded known-post or narrow X-only query and retain the actual retrieval route, tool trace, source identifiers/text extent and failure behavior. Do not use a model's narrative as proof of tool use or original source text.

Required inputs from the **operator, coordinated by Project Manager**:

1. A disposable test runtime or separate OS identity with an independently authorized Grok login and the required X access. Do not supply a copied live refresh token or modify the current user's login.
2. The allowed xAI/Grok login, refresh and X retrieval endpoints for that runtime, plus a permitted narrow test query or known post. This investigation did not infer those permissions from a local key's existence.
3. A way to inspect the effective tool/transport trace without publishing credentials, and the runtime's cleanup/credential-revocation owner.

Architect owns the next boundary investigation and evidence assessment. These are missing test inputs, not a request to approve a different product channel or remove X. If a safe login-backed path cannot be demonstrated, return the constraint and the above tradeoffs through Project Manager to Product Manager before changing access policy.

## Reproduction and verification limits

Use [q1-probe.py](q1-probe.py) on macOS with the exact binary digest above. It accepts `--binary`, `--root`, and a unique `--case`; existing case directories are rejected. It never reads the existing Grok auth store. Review the guard before running on a different machine; `/Users` and `sandbox-exec` are macOS-specific.

Representative commands, with local paths chosen by the operator:

```sh
python3 q1-probe.py --binary /path/to/pinned-grok --root ./q1-fixtures --case baseline-registry
python3 q1-probe.py --binary /path/to/pinned-grok --root ./q1-fixtures --case positive-read --tool read_file --arguments '{"target_file":"FIXTURE_PATH"}'
python3 q1-probe.py --binary /path/to/pinned-grok --root ./q1-fixtures --case deny-read --profile --tool read_file --arguments '{"target_file":"FIXTURE_PATH"}'
python3 q1-probe.py --binary /path/to/pinned-grok --root ./q1-fixtures --case context-profile --profile --seed-context
python3 q1-probe.py --binary /path/to/pinned-grok --root ./q1-fixtures --case context-profile-os-exec --profile --seed-context --deny-child-exec
```

The last option name denotes the tested executable restriction; it allows the pinned binary and does not forbid every descendant. The published harness includes the incremental controls used across cases. Earlier captures precede additions of later optional flags; those flags do not change the earlier case's request/dispatch behavior. The report does not claim every case ran with identical harness bytes. The selected result file records the actual observations, including failed setup and inconclusive checks.

For the OS controls, the same guard pattern was applied directly to `/bin/cat`, `/usr/bin/touch`, and `/usr/bin/nc`. Two local TCP listeners provided reachable allowed and denied ports, so a denied connection was not inferred from an absent server. The synthetic file outside the case directory provided the denied read/write target. Listeners were closed in the foreground.

Primary documentation read for configuration investigation: [official Grok settings](https://docs.x.ai/build/settings), [custom-model guidance](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-pager/docs/user-guide/11-custom-models.md), and [official CLI README](https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/codegen/xai-grok-shell/README.md). These sources guide fixture construction; the observed binary behavior above has the narrower applicability stated. In particular, a documented config option is not an executed login-backed test.

## Review, readiness and return

Author review completed for this evidence package using technical-design current-fact investigation and document-review: checked control effectiveness, exact binary identity, main versus auxiliary request classification, actual tool messages, canary outcomes, evidence limits, local references and the report's claims. Scripted assertions against the captured requests confirmed the 24-tool control, real positive read, five missing-tool responses, unchanged negative-case sentinels and both MCP startup outcomes. The OS results were inspected separately. This is not independent review or a product test suite.

At publication, the separate v1 review has returned NOT PASSED in ISSUE-6 comment `01a13454-4fce-7ce1-8164-fdc2e5dfa4eb`. Its TR1–TR7 findings and the separately queued substantive revision request `01a13457-5576-7245-9907-03358edf97c0` retain their own scope; this investigation does not close them. In particular, Q1-F1 supports examining the shared execution boundary but does not itself resolve TR1. The review remains bound to exact design v1 `060643a`, not this evidence package. The main design and original evidence are unchanged. No technical approval is asserted and no task plan or product implementation is created.

| Scope / stage | Current readiness | Next action |
| --- | --- | --- |
| Local custom-model registry and five dispatch checks | Evidence obtained for the pinned binary and stated configuration | Reviewer/Architect may use the observations within those limits. Do not generalize to the hosted login path. |
| Profile-only process isolation | Not established; Q1-F1 contradicts sufficiency | Evaluate clean configuration and a real OS/process boundary before credentials or source ingestion. |
| Login-backed X-only retrieval and X isolation architecture | DRAFT; Q1 OPEN; no affected architecture approval, task breakdown or coding readiness | Operator supplies the isolated test inputs; Architect runs the bounded checks above. |
| Shared core/non-X scope and delivery boundary | Task-breakdown readiness remains No; applicable v1 approval blockers remain under the separate review | The already queued substantive revision handles TR1–TR7; Project Manager combines that result with this evidence and coordinates affected review. This report does not clear any reviewed scope. |
| Complete first release | No acceptance or activation readiness | Preserve all F1–F9/SC1–SC8 obligations, including X. |

Return: Project Manager on ISSUE-6, referencing coordination ISSUE-5. The immediate next function is technical-design overall continuation of Q1 with the stated operator inputs, alongside disposition of the independent v1 review. The professional finding and evidence are delivered; Q1, technical approval and planner remain pending.
