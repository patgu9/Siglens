# Overall v1 investigation and document-check evidence

Date: 2026-10-13. Author: Engineering Lead / Architect. Applies to [technical-design.md v1](../technical-design.md), with its exact delivery commit recorded on ISSUE-6. This is design evidence, not a product test report or an independent review.

## Baselines and context

- Product/code start: `9c16ff29cf26d96ea126fbbb09494a91aae613d4`.
- Product approval-record revision examined: `239b9c382afb5620ab5badfd3fed7363049f5c74`; not adopted as a different behavior baseline.
- Isolated design branch: `agent/engineering-lead/7f5b05595ff8`.
- `git ls-tree -r --name-only HEAD` at start listed only LICENSE and product-design.md. Status/index were clean. Another worktree held the product author's branch and was not modified.
- Current issue and source issue were read through Multica CLI, using a roots-only summary followed by the relevant source thread. Product approval source and disclosure were inspected, not inferred from a filename or status.
- Workspace technical-design Skill ID `de061135-1554-49fe-901f-820bb6d97d6a` had the requested update timestamp `2026-10-12T20:40:42Z`. The missing local artifact-layout reference was retrieved through `multica skill get 5b91a4aa-d467-46de-8be5-9e12241022b8 --with-content --output json`.

## Bounded investigations

| Question / stopping condition | Procedure and observed result | Limit |
| --- | --- | --- |
| Can one local transaction support archive revision checks and exclusive claims? Stop at storage-mechanism feasibility. | Python subprocess probe below, exit 0. Python 3.14.7; SQLite 3.53.4. Four primitive checks passed. [SQLite transaction](https://www.sqlite.org/lang_transaction.html) and [atomic-commit documentation](https://www.sqlite.org/atomiccommit.html) were read. | Not Python 3.12 compatibility, product recovery, actual disk-full/power-loss durability, parallel race coverage, or remote delivery. |
| Why can five-level Jev scores be fractional? Stop at protocol semantics. | Read [official Score](https://docs.typesafe.ai/primitives/score) and [API reference](https://docs.typesafe.ai/api). Five criteria are indexed 0–4; response score is a probability-weighted position. Preserve returned score/probabilities/confidence and returned model identity. | No authenticated request, rubric evaluation, threshold-quality result or provider availability claim. General provider advice to combine dimensions does not override Siglens' prohibition on weighted rejection. |
| Can last30days supply the X isolation evidence for this runtime? Stop if the examined evidence does not cover its build. | Pinned upstream `50998cd1ba583f13a63b20e3fb5d906c71c31655`; inspected [grok_x.py](https://github.com/mvanhorn/last30days-skill/blob/50998cd1ba583f13a63b20e3fb5d906c71c31655/skills/last30days/scripts/lib/grok_x.py) and [boundary tests](https://github.com/mvanhorn/last30days-skill/blob/50998cd1ba583f13a63b20e3fb5d906c71c31655/tests/test_grok_tool_boundary.py). Source restricts support to Grok 1.0.46 build 2765805b9442; local `grok --version` returns 1.0.52 build 0920c8169e27. `grok --help` and `grok inspect --help` expose configuration controls, not isolation proof. | Upstream tests inspected use mocked invocation; they were not run here and cannot prove this binary's tool boundary. No account login, credential files, model prompt, tool invocation or paid research call used. Q1 remains open. |
| Is local distribution consistent with the required mechanism? | Read [uv tool guidance](https://docs.astral.sh/uv/guides/tools/); `uv` is available locally. | No Siglens package exists yet; installation was not attempted. |

The initial web search surfaced an independently operated Jev API site. Its own disclaimer identifies it as independent of the underlying model; it was not used to establish protocol. TypeSafe's official site links the documentation cited above. Documentation establishes declared capability, not live performance or quality.

## Product-record and document checks

Python read both product revisions with `git show` and compared complete rule/example/SC lines. Results: 52 rule lines unchanged, 106 example lines unchanged, 8 SC lines unchanged. Removing only Status/Approval and the question-record/Next Action region left identical remaining text. Q95–Q97 rows also remained byte-for-byte identical. The new record revision therefore does not introduce a new product behavior baseline for this design.

Mechanical checks on technical v1 verify ten numbered main sections in order and validate explicit F/SC references against the pinned product document. The Section 3 coverage ranges were expanded to check all rules and examples. Relative artifact links were checked after this evidence file was created. `git diff --cached --check` checks the delivered document changes. These checks do not establish semantic correctness; author review in Section 9 supplies its actual scope and limits.

The product design's previous structure validator exited 1 due to the known cross-Feature F7-E9 restriction. This investigation did not rerun it or relabel it as passing. No automated technical-design validator is supplied by the Skill. Mermaid rendering was not performed.

## Storage probe reproduction

Run this isolated probe with Python on local storage. It creates and closes its own temporary database and does not read a product store. The child uses abrupt process exit before commit; that is different from an operating-system crash or power loss. The uniqueness checks use two connections sequentially, not a simultaneous race.

```python
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    db = str(Path(directory) / "probe.db")
    connection = sqlite3.connect(db)
    connection.executescript("""
    PRAGMA journal_mode=DELETE;
    PRAGMA synchronous=FULL;
    CREATE TABLE archive (id INTEGER PRIMARY KEY, revision INTEGER, body TEXT);
    INSERT INTO archive VALUES (1, 4, '{"state":"active","sets":["AI"]}');
    CREATE TABLE claims (edition TEXT, target TEXT, owner TEXT, epoch INTEGER,
                         PRIMARY KEY (edition,target));
    """)
    child = subprocess.run([sys.executable, "-c", """
import os, sqlite3, sys
c = sqlite3.connect(sys.argv[1])
c.execute('BEGIN IMMEDIATE')
c.execute('UPDATE archive SET revision=5, body=? WHERE id=1',
          ('{"state":"ordinary","sets":[]}',))
os._exit(17)
""", db], check=False)
    assert child.returncode == 17
    row = connection.execute("SELECT revision,body FROM archive WHERE id=1").fetchone()
    assert row[0] == 4
    assert json.loads(row[1]) == {"state": "active", "sets": ["AI"]}
    connection.execute("UPDATE archive SET revision=5 WHERE revision=4")
    connection.commit()
    assert connection.execute("UPDATE archive SET revision=6 WHERE revision=4").rowcount == 0
    connection.execute("INSERT INTO claims VALUES ('E1','target','A',1)")
    connection.commit()
    other = sqlite3.connect(db)
    try:
        other.execute("INSERT INTO claims VALUES ('E1','target','B',1)")
        raise AssertionError("duplicate claim accepted")
    except sqlite3.IntegrityError:
        other.rollback()
    connection.execute("UPDATE claims SET owner='B',epoch=2 WHERE epoch=1")
    connection.commit()
    assert other.execute("UPDATE claims SET owner='A' WHERE epoch=1").rowcount == 0
    other.close()
    connection.close()
    print(sys.version.split()[0], sqlite3.sqlite_version, "four primitive checks PASS")
```

Observed result from both the workdir-local probe and a separate execution of the exact delivered snippet: exit 0, Python 3.14.7 / SQLite 3.53.4, all four primitive checks PASS. The second execution verifies the reproduction text. This is not a reusable product implementation.
