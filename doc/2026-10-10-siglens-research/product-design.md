## Design Doc : Siglens Research, Event Archive, and Daily Brief

- Status: APPROVED
- Version: v2
- Approval: v2 | 2026-10-12 | Human owner | [Approval record](technical-design.md#9-review-and-approval)
- Mode: Builder
- Date: 2026-10-12
- Stage: Think

**Approval update:** The owner approved this v2 as the planning baseline on 2026-10-12. The [approved content snapshot](history/product-design/v2.md) preserves the exact reviewed bytes. Earlier review/approval wording below records the pre-approval history; it does not override this approval. Product rules and examples are unchanged by this update.

**Revision v2:** This version clarifies fractional-window card limits and uncertain event-time eligibility under Q88. [Preserved v1](history/product-design/v1.md) retains the prior baseline.

### Glossary

| Term | Definition |
|-----|-----|
| CLI | Command-line interface used by host Agents to execute validated plans, save state, and check deliverables. |
| Jev | Structured judgment service used for Discovery candidate review. It does not generate reports or establish facts. |
| UTC | Coordinated Universal Time, used to store event-window instants. |
| Comparable | Future research entrypoint for comparing several explicit objects using each object's evidence. Outside this first release. |
| Domain | Required scope for Discovery, such as AI or biotechnology. A domain is not a discovered event. |
| Discovery | Find concrete events or substantive developments within a domain. Deliver topic cards after limited evidence enrichment. |
| Named-Topic | Research a topic supplied directly by the user. Deliver a structured report without nomination or candidate review. |
| Topic Research | Shared investigation capability used by selected Discovery candidates and direct Named-Topic requests. These uses have different deliverables. |
| Topic | A specific object, event, change, or question worth investigating. Its research value does not establish its truth. |
| Event | The archived identity linking a concrete occurrence and its later developments across research runs. Agent judgment determines these links. |
| Nomination | A named candidate with initial evidence. It has not yet completed candidate review or enrichment. |
| Candidate Review | Jev-assisted review after nomination and before enrichment. The Agent makes the final selection. |
| Enrichment | Limited Topic Research to obtain context, check claims and event time, and attempt checks across channels. |
| Evidence | Saved material traceable to an original source. Distinguish source text, extracts, abstracts, search snippets, and Agent synthesis. Model scores are not evidence. |
| First-party Evidence | Material from an event participant or original researcher. It supports only the claims it directly establishes. |
| Research Window | Event/development start and end fixed when a run is created. Resume, enrichment, and refresh keep them. Later heat observation times have a separate freshness boundary. |
| Event Time | When an event or substantive development happened. Collection and repost times cannot replace it. |
| Background Evidence | Material outside the research window used for context. It does not count as a recent development. |
| Topic Card | One event or development, its research value, event time and basis, original links, confirmed and uncertain claims, and next research question. |
| Research Report | A structured answer to a user-supplied topic, with questions, findings, evidence, and limits. Completion does not imply that every claim is confirmed. |
| Event Archive | Persistent event identities, evidence versions, past judgments, open questions, and tracking states shared across runs. |
| Heat Observation | A source metric with its meaning, platform, event link, and observation time. Current heat is distinct from measured growth. |
| Briefing | Research content supplied for external delivery: developments, heat observations, follow-ups, evidence references, and coverage gaps. |
| Edition | An immutable finalized research deliverable with a stable identity. A correction creates a new edition and links the prior one. |
| Daily Brief | A daily presentation of a Briefing in Multica, organized by the external Agent workflow. |
| Delivery Claim | Exclusive local permission for an external workflow to send one edition to one target. It does not itself send a network message. |

### Background

#### Problem Statement

The initial user, patgu9, manually reads X and communities to keep up with AI developments. Channels contain different information. Separate searches make it hard to connect yesterday's uncertain claim with today's new evidence. Siglens should provide a daily brief that supports further investigation and preserves this continuity.

- **Evidence:** The [retained pre-migration document](history/product-design/pre-layout-2026-10-12.md) summarizes historical interviews through Q78, the event archive design, and later decisions. The user requested deletion of the original historical files on 2026-10-10. Those files and their original approval records are unavailable; their summaries do not approve this version. Q79–Q83 below cite the user's answers in this conversation. Repository inspection on 2026-10-12 found documentation and no product source, package, or tests. No reading-time baseline, channel/model evaluation, or delivery trial exists.
- **Constraints (optional):** Rebuild the requirements at Think stage. Keep prior decisions traceable and keep this version unapproved until reviewed. Use English search and research output. Adopt a Skill and an independent Python 3.12+ CLI installed through `uv tool`; Multica is the initial reading destination, not a required CLI dependency.

#### What Makes This Cool

Today's brief connects to yesterday's events. The reader sees popular topics alongside important releases with little engagement. Follow-ups explain which fact, evidence, or judgment changed. Original links and explicit gaps let the reader inspect the basis and ask another research question.

### Solution Design

#### Approaches Considered

| Approach | Core Idea and Benefits | Main Costs and Risks |
|-----|-----|-----|
| A: Batch briefs with an explicit tracking list | Reuse research and saved files. Produce each brief separately and manually attach past references. Closest minimal alternative to manual searches. | Effort: L; risk: Medium. Less archive work, but repeated reading and manual linking weaken continuity. Rejected in the approved event design. |
| B: Event archive with continuous briefs | Reuse collection and evidence ideas from last30days. Add persistent event relationships, corrections, and follow-ups while keeping a local CLI and external orchestration. | Effort: XL; risk: High. Event identity, evidence changes, and delivery uncertainty add work. Selected in the approved event design. Reuse remains unverified. |
| C: Service with a shared graph and prediction system | Centralize subscriptions and relationships for many readers; offer long-term trend analysis. | Effort: XL; risk: High. Adds services, operating cost, and assumptions about demand. Deferred by the later plan; unnecessary for one reader. |

These sizes compare the recorded scope; they are not calendar estimates. No implementation measurements support delivery dates. Continuing manual reading avoids build work but leaves the stated continuity problem unresolved. Prior last30days research used a fixed 2026-09-28 inspection; it does not establish current service availability or proven reuse.

#### Recommended Approach

**Recommendation:** Retain B, the previously selected event archive and continuous brief. Keep Discovery and Named-Topic, seven supported channels, separate heat observations, and external delivery. This reconstruction carries forward product decisions and incorporates Q79–Q83 from this conversation; it does not renew the old implementation approval.

**How It Works:**

1. The host Agent uses the CLI guide to understand inputs and recovery (F8; SC8). The user or external workflow requests domain Discovery or supplies a Named-Topic. The Agent submits a plan; the CLI fixes the window and checks channel readiness (F1, F2; SC1, SC2). The reader can inspect coverage instead of assuming a complete scan.
2. For Discovery, the Agent merges materials into nominations. The CLI calls Jev; the Agent selects candidates (F3; SC3). The reader gets concrete leads rather than raw posts. Direct Named-Topic starts Topic Research here without candidate review.
3. The CLI executes evidence plans. The Agent checks claims, interprets gaps, and decides whether another finite round is needed (F4; SC1, SC3). The reader can inspect original sources and distinguish known facts from open questions.
4. The Agent links events and proposes corrections to the archive. The CLI records revisions and heat observations; the Agent prepares the Briefing (F5, F6, F7; SC4, SC5). The reader can connect new evidence to prior editions without treating popularity as proof.
5. The CLI finalizes an edition and grants a local delivery claim. The external workflow sends it through Multica CLI and returns a receipt (F8, F9; SC6, SC7). The reader receives a traceable brief, while retries preserve research and avoid duplicate delivery. The Skill guides Agent choice, handoffs, and orchestration; the CLI supplies data and validation.

**Scope:**

- Initial audience: patgu9 using an AI daily brief in Multica. Domain Discovery remains usable for other explicit domains; it has no global mode. The smallest useful outcome is two consecutive briefs that link an event and explain a new piece of evidence.
- Included: F1–F9, both research entrypoints, all seven channel adapters, evidence retention, Jev review, event corrections, focus tracking, source heat lists, local Briefing, recovery, and delivery reconciliation. A two-brief demonstration does not replace complete research acceptance.
- Distribution: install the independent CLI locally with Python 3.12+ and `uv tool`; provide the Skill and CLI Agent guide. External tools transfer files or accessible content to successor Agents. Do not assume different runners share a directory.
- Excluded: full Comparable, browser fallback, collection/Jev spending quotas, a weighted four-dimension rejection score, scoring `unknown` or assessability Choice, CLI Agent scheduling or automatic model upgrades, cross-machine transport or dedicated research-package import/export, automatic evidence expiry, a dashboard, combined cross-platform heat scores, heat prediction, a graph service, and public package release.
- Ownership: Agent judgment covers event identity, evidence support, selection, synthesis, and research sufficiency. CLI validation covers executable plans, references, counts, timestamps, stored state, and delivery records. External workflow owns timing, daily organization, runtime/model choice, network publication, and handoff transport.

**Premises and Open Questions:**

| Type | Statement and Impact | Evidence / Validation Status | Follow-up |
|-----|-----|-----|-----|
| Baseline and layout migration | Migrate the existing research change to the new task layout. Affected content: paths, metadata, Q records, and evidence descriptions. Blocks approval: No, because the user authorized analysis and migration; product rules remain unchanged. | Source: [unversioned English baseline](history/product-design/pre-layout-2026-10-12.md), dated 2026-10-10, Status IN_REVIEW; no exact-version approval. Also retain the [original Chinese reading copy](history/product-design/pre-layout-2026-10-12-zh.md). Request: user asked on 2026-10-12 to analyze the current requirements and adopt the new directory standard. v1 is the first tracked version, not an invented historical version. | Use product-design.md as the current authority. [Chinese reading copy](product-design-zh.md) follows this v1 and cannot independently change decisions. User confirmation is pending. |
| Accepted premise | Prior research decisions remain in scope. Affected content: F1–F4, F8. Blocks approval: No, because the migration retains the documented baseline. | Retained source summary: Q12 requires a domain; Q31 includes Named-Topic; Q60 excludes browsers; round 20 removes quotas; Q69 removes scoring unknown; Q77 limits Brave; Q78 fixes windows. Original answer records were deleted at the user's request; this is a retained summary, not accessible approval evidence. | Preserve these rules. User reviews this complete v1 before any approved downstream handoff. |
| Accepted premise | Continuous briefs extend the original research scope. Affected content: F5–F9. Blocks approval: No, because the selected direction is unchanged. | Retained source summary: B was selected; platform/metric groups, 24-hour freshness, local evidence, and external network delivery were recorded. Q83 changes the observation-inside-event-window constraint. | Keep the product boundaries. Define engineering mechanisms only in a separately requested stage. |
| Assumption to validate | Cross-channel coverage improves discovery and evidence quality. Affected content: F2-AC1/AC2, F4-AC2; SC2. Blocks approval: No, because the user chose seven channels despite this uncertainty. | Not validated. Observe unique leads, added supporting/contradicting evidence, and omissions per channel using the known-event walkthrough in SC2. Counterexample: all channels are attempted but an important known event is missed, or added channels only repeat the same original source. Historical adapter notes do not establish live or historical coverage. | Researcher records per-channel contribution. If the counterexample occurs, reopen channel access and query plans under F2-AC1/AC2 and the coverage-value premise; bring any scope reduction to the user. Do not silently remove a channel. |
| Assumption to validate | Continuous briefs replace some manual reading. Affected content: selected B, F5, F7; SC4. Blocks approval: No, because Builder can try the outcome before relying on the assumption. | Not validated. After two real briefs, ask the reader which manual reading actions were replaced; collect concrete examples under SC4. Counterexample: the reader still has to repeat the same searches to understand changes, or follow-ups only repeat old links. No time baseline or savings target is agreed. | User and researcher inspect the missing context. If the counterexample occurs, reopen B's value, event continuity under F5-AC2, and Briefing content under F7-AC1. Do not treat a text walkthrough as a product trial. |
| Assumption to validate | Jev improves review without losing useful early signals. Affected content: F3-AC2/AC5/AC6; SC3. Blocks approval: No, because its role and threshold were selected but remain uncalibrated. | Not validated. Compare saved Jev suggestions and Agent decisions with labeled junk, thin evidence, low-engagement announcements, and threshold cases in SC3. Counterexample: a labeled useful first-party lead receives a low-value suggestion that the Agent accepts without examining its evidence, or a junk lead passes unnoticed. No numeric accuracy or false-rejection threshold is agreed. | Researcher defines and evaluates the rubric. If the counterexample occurs, reopen the criteria and threshold under F3-AC5/AC6 and Jev's role under F3-AC2 with the user. Changes require a separate decision; model-quality tests have not run. |
| Q79 / User decision / RESOLVED | How should a comparable group be ordered? Affected content: F6-AC3, F6-E4, SC5. Depends on: None. Blocks approval: No, because the user chose raw-value ordering. | Answer: option 1, "1", to Q79 in this conversation on 2026-10-10. Options: raw-value descending with times; additional publication-age groups; keep pending. Tradeoff: raw values are simple but favor accumulated engagement; age groups add comparison choices. Recommendation was raw-value descending for a traceable first release. | Preserve descending order and publication/observation times; no age adjustment or growth claim. Q81 defines comparable groups. |
| Q80 / User decision / RESOLVED | Which timezone and endpoint convention apply? Affected content: F1-AC2, F4-AC3, F1-E8. Depends on: None. Blocks approval: No, because the user chose UTC and a half-open interval. | Answer: "UTC 保存，包含起点、不含终点（推荐）", Q80 reply in this conversation on 2026-10-10. Options: UTC [start, end); UTC with both endpoints included; keep pending. Recommendation: [start, end) assigns an exact endpoint consistently; both-inclusive windows can share that endpoint. Daily seven-day windows still overlap. | Apply UTC [start, end). Q83 separates heat observation timing without moving the event window. |
| Q81 / User decision / RESOLVED | Which observations are comparable? Affected content: F6-AC3/AC4, F6-E9/E10, SC5. Depends on: Q79 for ordering computed groups. Blocks approval: No, because the user accepted metric separation. | Answer: "采用上述规则（推荐）", Q81 reply in this conversation on 2026-10-10. Options: same platform/metric meaning/unit with separate provider ranks; interaction values only; keep pending. Recommendation: separate provider positions preserves useful source data without mixing units. Interaction-only output would omit that context. | Keep provider positions separate from computed count rankings. The choice does not validate provider quality. |
| Q82 / User decision / RESOLVED | When should active unanswered questions be rechecked? Affected content: F5-AC3, F5-E3/E9, SC4. Depends on: None. Blocks approval: No, because the user chose each daily run. | Answer: "每次每日研究都尝试重查（推荐）", Q82 reply in this conversation on 2026-10-10. Options: every daily run; only after linked new material; external per-item timing. Recommendation: daily attempts support continuity but require more checks; new-material triggers save work but may leave a question unattended. | Record attempts and gaps on every daily run. Ordinary and paused states keep their existing boundaries; no promise of new evidence. |
| Q83 / User decision / RESOLVED; review R1 | Should heat observations use the event window or a separate freshness boundary? Affected content: F6-AC2, F6-E2/E3/E11, SC5. Depends on: Q80's fixed event window. Blocks approval: No, because the user chose separate boundaries. | Answer: "采用分开的边界（推荐）", Q83 reply in this conversation on 2026-10-10. Prior constraint: observations inside the event window. Review R1 reopened it because a newly created run rejects its later observations. Options: freshness through finalization; keep window-only observations. Recommendation: separate boundaries allow current first-run heat; window-only relies on available prior observations. | Preserve event eligibility. Observation must not be later than finalization and must be at most 24 hours old; no change to the event window. |
| Q88 / User decision / RESOLVED | How should fractional-day windows and uncertain event-time intervals be handled? Affected content: F1-AC3/AC4, F1-E9, F4-AC3, F4-E8. Depends on: Q80. Blocks approval: No for these policies; complete v2 approval remains pending. | Answer: "采用上述保守规则（推荐）" in the architecture conversation on 2026-10-12. Options: explicit card maximum for fractional days with fully contained event-time intervals; round window days up with fully contained intervals; remain unresolved. Recommendation: explicit limits and full containment avoid invented rounding or precise event times. | Apply the two confirmed policies. Q84–Q87 and Q89–Q90 are architecture records; Q88 is authoritative here. This answer does not approve all of v2 or the overall technical design. |
| Prior review findings R2/R3 / RESOLVED | Keep provider positions distinct and reader Event ID follow-up explicit. Affected content: F6-AC3/AC4/E9, F5-AC6/E8/E9. Blocks approval: No, because their remedies were reviewed in the prior invocation. | The retained baseline records two completed independent rounds on 2026-10-10. Round 2 confirmed these corrections. That review applies to its source text, not automatically to v1's new records. | Recheck the migration and complete v1 review; keep the original rule/example IDs. |
| Configuration to supply | Schedule, timezone, Multica target, and issue organization are external deployment inputs. Affected content: F9-AC1/AC2. Blocks approval: No, because scheduling belongs to the external workflow and activation is not requested. | No destination or activation time is supplied. The retained baseline assigns these inputs to the external Agent. | Supply and verify them before enabling delivery; this invocation creates no schedule or message. |
| Contract detail to define | Commands, schemas, citation locations, operation identities, package name, and adapter/model protocols remain engineering work. Affected content: F2, F3, F5, F8, F9. Blocks approval: No, because product outcomes and ownership are defined. | Repository has no working interface. X/Grok access, Digg data, crash recovery, and Multica reconciliation require live or implementation evidence. | Architect defines contracts and verification in a separately requested overall technical design, after approval of this version. |
| Presentation boundary | About 1,200 words and mandatory attachment splitting are not fixed requirements. Affected content: F7-AC3. Blocks approval: No, because local storage and optional distribution are the retained requirements. | Source summary: an earlier layout proposed a soft length and attachments; later user direction confirmed local evidence and permitted brief output or attachments. No hard length is confirmed. | Ask for a numeric presentation target only if needed. Preserve counterevidence and gaps. |
| Migration finding M1 / REPAIRED | Clarify the Chinese reading copy's window and orchestration wording. Affected content: Chinese SC1, F4-AC4/E7, F8-E4, F6-E3. Blocks approval: No, because the English authority already fixes the behavior. | Independent migration round 1 found that the translation could imply an execution deadline or permit autonomous finite CLI rounds. Those passages now state the original window is reused and the CLI does not start another round. | Recheck the translated passages; no new product decision or English rule change. |
| Architecture feedback Q88 / APPLIED in v2 | Clarify two edge policies without changing other Feature rules. Affected content: F1-AC3/E9 and F4-AC3/E8. Blocks approval: No for these confirmed policies; complete v2 approval is pending. | User confirmed both policies on 2026-10-12. v1 is preserved in history/product-design/v1.md. Self-review checked the two changed rules, two new examples, and architecture mappings; no new independent review or product test ran. | Review the complete v2 baseline before approved downstream handoff. Earlier v1 review statements describe that historical version only. |
| Review coverage | v1 awaits explicit user approval. Blocks approval: No, because no product decision is reopened. | Prior baseline: two completed independent rounds, R1–R3 resolved. Migration: full self-review and one completed independent round; only translation finding M1 required repair. Structure, links, snapshots, Q records, and unchanged English behavior pass. Product/channel/model/delivery tests have not run. | Independently recheck M1 and deliver this v1 for user review; review does not grant approval. |

**Next Action:** Walk through F5-E2 and F7-E1 as two consecutive brief examples and identify whether the second brief explains a useful change without rereading the first.

#### Success Criteria

| ID | Desired Outcome and Pass Condition | Measurement Context and Method |
|-----|-----|-----|
| SC1 | Both entrypoints produce their own deliverable with a fixed window, evidence links, and explicit uncertainty. | One domain Discovery and one direct Named-Topic demonstration; inspect F1 and F4 examples. Not executed. |
| SC2 | The reader can distinguish each channel's readiness, selection, results, failure, retrieval route, and evidence extent. | Seven-channel known-event sample, including a failure and a healthy empty query. Compare unique leads, added evidence, and omissions. No completeness percentage is claimed. |
| SC3 | Useful low-engagement leads survive review, while pure speculation is excluded. Failed scoring never fabricates a low score. | Labeled examples and Jev response fixtures under F3; live model quality is measured separately. No approved numeric accuracy target exists. |
| SC4 | Two consecutive briefs share event identities and explain new evidence, corrections, or no observed change. The reader identifies an actual reading task replaced. | Two real daily runs after implementation, plus correction fixtures. Until then, examples illustrate intended behavior only. No invented time-saving target. |
| SC5 | Heat is traceable and separate from research value and fact status; stale or insufficient samples do not produce invented rankings. | Fixtures at 24 hours and above, event eligibility versus later observation times, future timestamps, missing values, one/two samples, descending order, and separate count/provider-rank views. Not executed. |
| SC6 | Retries preserve success, healthy empty results, prior archive history, and drafts without silently overwriting newer state. | Interrupted collection and stale/concurrent write fixtures. Inspect visible state and old references before and after recovery. |
| SC7 | One edition and target have a reconciled delivery record; response loss does not cause blind reposting. | External Multica workflow trial with success, known failure, and lost receipt. Simulated behavior and real delivery are recorded separately. |
| SC8 | An Agent can install and operate the independent CLI through its guide and default JSON responses without installing Multica. | Clean Python 3.12+ local installation through `uv tool`, then both entrypoints. No startup-time promise or public release is implied. |

### Requirements

#### Feature 1 — Start a scoped research run

##### User Story

> In order to investigate a clear question within a stable period,
> as a researcher,
> I want to start domain Discovery or direct Named-Topic research.

- **Related Success Criteria:** SC1, SC8.

##### Rules

- **F1-AC1:** Discovery requires a domain. Named-Topic requires a user-supplied concrete topic and uses Topic Research directly. Do not relabel a discovered candidate to evade its review requirements.
- **F1-AC2:** Default to the recent seven days. Save start/end instants in UTC; include the start and exclude the end (Q80). Resume, enrichment, and explicit refresh retain them. A new current window requires a new run; daily seven-day windows may overlap.
- **F1-AC3:** Use English search and research deliverables, preserving original evidence links. Discovery card count is configurable; for a whole number of 24-hour days, the default maximum is window days multiplied by three. A fractional-day window requires an explicit integer card maximum (Q88). It is neither a collection quota nor a required daily count.
- **F1-AC4:** The Agent submits a structured plan. The CLI validates and executes it. Invalid inputs return the problem and a correction action without committing an invalid run or plan.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F1-E1: Missing domain | F1-AC1, F1-AC4 | Discovery request has no domain. | Start research. | Reject it with the missing input; no invalid run is committed. |
| F1-E2: Direct research | F1-AC1 | User asks whether fictional Model Z has shipped. | Start Named-Topic. | Enter planned Topic Research without nomination/Jev review; do not assume it shipped. |
| F1-E3: Candidate relabel | F1-AC1 | Discovery candidate C1 lacks review or a recorded Jev failure. | Submit it as a direct-topic result without a user request. | Its Discovery origin still requires review; changing a label is insufficient. |
| F1-E4: Next-day resume | F1-AC2 | R1 has saved start S and end T. | Resume tomorrow, enrich, or refresh. | Keep S and T; a request ending tomorrow creates another run. |
| F1-E5: Upper limit | F1-AC3 | Seven-day run; default maximum; 23 eligible developments. | Select final cards. | Agent selects at most 21 English cards; the two unselected items are not labeled junk. |
| F1-E6: Few results | F1-AC3 | Seven-day run finds four eligible events. | Prepare results. | Deliver four cards; do not invent 17 or require three per day. |
| F1-E7: Invalid plan | F1-AC4 | R1 exists; submitted plan contains an unsupported channel. | Validate the plan. | Explain the channel error; prior committed plan and results remain intact. |
| F1-E8: Exact endpoints | F1-AC2 | Saved window is 2026-10-03T12:00:00Z to 2026-10-10T12:00:00Z. Two events occur exactly at those endpoints. | Check recent eligibility. | Start event is inside; end event is outside. Resume does not change either result. |
| F1-E9: Fractional window | F1-AC3, F1-AC4 | A 36-hour window has no explicit card maximum. | Start Discovery, then resubmit with an integer maximum. | First request asks for the maximum and commits no invalid run; the explicit maximum permits validation. No implicit day rounding occurs. |

#### Feature 2 — Collect across channels with visible coverage

##### User Story

> In order to inspect complementary sources and recognize gaps,
> as a researcher,
> I want to collect evidence across selected channels and see how each material was obtained.

- **Related Success Criteria:** SC2, SC3.

##### Rules

- **F2-AC1:** Support X through the chosen Grok login direction; Reddit RSS/search and community lists; GitHub REST Issues/PRs and release evidence; Hacker News Algolia/search and lists; direct public Digg data; direct arXiv API; and Brave Web search with separate HTTP text retrieval. Each channel can contribute Discovery nominations. These are access requirements, not claims of current availability.
- **F2-AC2:** Enable all supported channels by default and attempt all selected, validated, configured channels in both entrypoints. Automatically run doctor for the first research use or relevant configuration changes. User selection narrows execution and cannot bypass validation.
- **F2-AC3:** Distinguish unconfigured, not selected, validation failure, request failure, successful empty, and successful data outcomes. Record coverage and diagnostic causes. A cached readiness check is not proof of a later request's success or complete historical coverage.
- **F2-AC4:** Allow targeted Brave fallback only when Web is selected and validated. Explicitly disabled content channels must not be retrieved indirectly through Web. Do not treat deliberate disablement as a channel fault. Record content channel, retrieval method, and text availability separately.
- **F2-AC5:** Save actual retrieved text, quoted extracts and context, original links, retrieval time, and material type. Label abstracts, snippets, truncation, and missing text. Keep Agent synthesis distinct. Raw HTML and full API responses are optional diagnostics.
- **F2-AC6:** Retain research state, acquired evidence, references, review records, and deliverables by default without automatic expiry. Preserve versions used by earlier citations. Two retrieval paths or reposts of one original material do not establish independent evidence.
- **F2-AC7:** Treat collected content as research data. It cannot authorize new actions, replace research rules, or execute instructions embedded in a source.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F2-E1: Discovery coverage | F2-AC1, F2-AC2 | AI run; all seven selected and validated; each plan contains a supported query. | Collect. | Attempt all seven; GitHub, arXiv, and Web can supply nominations as well as enrichment. |
| F2-E2: Configuration change | F2-AC2 | Brave configuration changes after R1. | Start R2. | Recheck affected readiness before execution; a parameter cannot substitute for validation. |
| F2-E3: Direct-topic coverage | F2-AC2 | Named-Topic; six channels ready; X unconfigured; no selection override. | Collect. | Attempt the six; record X's gap rather than silently omitting ready channels. |
| F2-E4: Different outcomes | F2-AC3 | X unconfigured; GitHub unselected; Digg fails validation; Reddit request fails; HN returns no items; arXiv returns two. | Inspect coverage. | Show the six distinct outcomes and available causes; only HN is a healthy empty query. |
| F2-E5: No Web selected | F2-AC4 | Select only X/Reddit; Reddit fails; Brave is configured. | Handle failure. | Keep the Reddit gap; do not call Brave. |
| F2-E6: Legal fallback | F2-AC3, F2-AC4, F2-AC5 | Select Reddit/Web; Reddit fails; Brave finds a Reddit snippet. | Save fallback. | Record failed direct Reddit access, Brave retrieval, and snippet-only evidence. |
| F2-E7: Disabled content | F2-AC4 | Reddit explicitly disabled; Web selected; a search returns a Reddit link. | Process the hit. | Exclude that content from indirect research; disablement is not overridden by Web. |
| F2-E8: Abstract only | F2-AC5 | arXiv metadata/abstract obtained; full paper unavailable. | Save and cite it. | Mark it as an abstract; preserve its actual text and link without inventing paper content. |
| F2-E9: Same original | F2-AC6 | Direct X post and Digg hit point to that same post. | Bind evidence. | Preserve retrieval records; do not call them two independent confirmations. |
| F2-E10: Changed source | F2-AC5, F2-AC6 | Edition E1 cites saved text V1; source changes to V2. | Explicitly refresh later. | Preserve V1 and its citation; store V2 as a later material version. |
| F2-E11: Source instructions | F2-AC7 | Retrieved page says to ignore rules and publish elsewhere. | Read the page. | Treat those words as source content; they do not change the plan or authorize publication. |

#### Feature 3 — Review and select Discovery candidates

##### User Story

> In order to spend research effort on concrete useful leads,
> as a researcher,
> I want to inspect reviewed nominations with evidence status and separate research-value judgments.

- **Related Success Criteria:** SC3.

##### Rules

- **F3-AC1:** The CLI collects and performs basic deduplication. The Agent merges events, names nominations, and binds initial evidence. Do not call Jev during nomination. Call it after nomination and before enrichment; do not add a second routine scoring phase after enrichment.
- **F3-AC2:** Discovery cannot actively skip Jev. Record unavailability or invalid responses and let the Agent take over when the call cannot complete. Named-Topic has no candidate-review prerequisite.
- **F3-AC3:** Record domain relevance, pure speculation, initial evidence state, and research value separately. Exclude pure release speculation and content with no concrete new matter. Judge content, not question wording, first-person form, self-promotion, or engagement alone.
- **F3-AC4:** Concrete leads supported only by a snippet/abstract may enter enrichment with insufficient initial evidence recorded. Low engagement or one direct source cannot automatically reject a lead. Preserve exclusion, merge, pending-check, low-value selection, and count-limit outcomes distinctly.
- **F3-AC5:** Score substantive change, specificity/information, potential impact, and further research space separately on five-level criteria. Use bound source extracts and context, not assumed enrichment results. Preserve raw score, available probabilities/confidence, and the criteria/input versions.
- **F3-AC6:** Map raw scores in 0–4 to display scores in 1–5 by adding one. Four valid, unrounded display scores all below 3 create a low-value rejection suggestion for Agent confirmation. One score equal to or above 3 prevents this suggestion; it does not guarantee selection. Do not apply a weighted total rejection rule.
- **F3-AC7:** Do not add scoring unknown or assessability Choice, multiply by confidence, or turn low confidence into a missing score. Call failures and invalid dimensions cannot fabricate zero, minimum, or midpoint scores, and cannot satisfy the four-low-score condition.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F3-E1: Stage order | F3-AC1, F3-AC5 | Three posts describe Model Z release. | Nominate, review, then enrich. | Agent binds one nomination; Jev sees current extracts once at candidate review; enrichment does not automatically score again. |
| F3-E2: Intentional skip | F3-AC2 | Jev available; Discovery workflow requests no review to save cost. | Submit final cards. | Missing review blocks finalization; this is not a service-unavailable exception. |
| F3-E3: Jev timeout | F3-AC2, F3-AC7 | Jev call times out. | Continue review. | Save failure/degradation; Agent takes over; no manufactured scores or low-value trigger. |
| F3-E4: Popular rumor | F3-AC3 | Many posts only guess that Model Z will ship tomorrow. | Review. | Exclude pure speculation even if interaction is high. |
| F3-E5: Question with a real event | F3-AC3 | A help post contains a reproducible new outage and source details. | Review its content. | Investigate the outage; question form alone does not mark it junk. |
| F3-E6: Thin first-party lead | F3-AC4 | Official release snippet; no interactions; only one source. | Select for enrichment. | It may proceed with evidence limits recorded; low engagement and source count do not reject it. |
| F3-E7: All below midpoint | F3-AC6 | Raw scores 1.4/1.7/1.1/1.99; all valid. | Compute suggestion. | Display 2.4/2.7/2.1/2.99; suggest rejection for Agent confirmation despite rounded display possibly showing 3. |
| F3-E8: Exactly midpoint | F3-AC6 | Raw scores 1.4/1.7/2.0/1.8. | Compute suggestion. | Display dimension 3 is exactly 3; no four-low-score suggestion; Agent still chooses. |
| F3-E9: Invalid dimension | F3-AC6, F3-AC7 | Three valid low scores; fourth missing or outside range. | Validate response. | Record failure; no invented fourth score or four-low-score suggestion. |
| F3-E10: Diffuse distribution | F3-AC5, F3-AC7 | Valid score 2.7 with low confidence and saved probabilities. | Interpret it. | Preserve display score 3.7 and the distribution; no scoring unknown or confidence multiplier. |
| F3-E11: Different dispositions | F3-AC4 | One rumor, one duplicate, one unknown-time lead, one eligible card over the limit. | Save decisions. | Record exclusion, merge, pending check, and eligible-but-unselected separately; retain materials. |

#### Feature 4 — Investigate a topic and explain uncertainty

##### User Story

> In order to understand what evidence actually establishes,
> as a researcher,
> I want to investigate topics, answer questions, and expose remaining uncertainty.

- **Related Success Criteria:** SC1, SC2, SC3.

##### Rules

- **F4-AC1:** Reuse Topic Research for selected Discovery candidates and direct Named-Topic. Discovery needs limited enrichment and topic cards, not a full standalone report for every candidate. Named-Topic delivers a structured English report with questions, findings, evidence, and limits; exact chapter titles are not fixed requirements.
- **F4-AC2:** Attempt checks across channels and keep the attempts and outcomes. Do not require two independent sources. First-party evidence can establish its direct claim, but cannot establish untested effects or comparisons merely by association.
- **F4-AC3:** Use event/development time for recent eligibility. Keep outside-window material as labeled background. If event time remains unknown after checking, retain the candidate and missing basis but exclude it from final recent cards. When evidence supports only a time interval, the entire possible occurrence interval must lie inside the research window; retain boundary-overlapping intervals as pending rather than inventing a precise instant (Q88).
- **F4-AC4:** The Agent may submit further finite plans and decides research sufficiency. The CLI does not initiate research loops or stop after an invented no-progress round count. Named-Topic may conclude that a claim cannot currently be confirmed; lack of confirmation is not proof of absence.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F4-E1: Shared capability | F4-AC1 | Discovery selects C1; user separately supplies Topic T1. | Investigate both. | C1 receives limited enrichment/card output; T1 receives a report; both use saved evidence plans. |
| F4-E2: Single direct source | F4-AC2 | Official repository confirms release; other-channel checks find no independent test. | Write findings. | State that release is supported; disclose checks/gaps; performance superiority remains unconfirmed. |
| F4-E3: Old repost | F4-AC3 | Release occurred months before saved window; repost occurs strictly inside it. | Assess recency. | Old release is background; repost time does not make it a new release. |
| F4-E4: New development in old event | F4-AC3 | Archived old release; independent test published strictly inside the new window. | Investigate the new result. | The test can be a recent development with its own time basis; release evidence is background. |
| F4-E5: Unknown time | F4-AC3 | Concrete lead still lacks event time after enrichment. | Prepare recent cards. | Retain pending candidate and missing basis; omit it from recent cards. |
| F4-E6: Cannot confirm | F4-AC1, F4-AC4 | Named-Topic asks about a supposed launch; accessible evidence is inconclusive. | Complete report. | Explain searches, evidence, and gaps; say cannot currently confirm, not proved nonexistent. |
| F4-E7: Another question | F4-AC4 | First finite plan leaves a specific evidence gap. | Agent submits another plan. | CLI validates and executes it with the same window; no autonomous research loop starts. |
| F4-E8: Uncertain time interval | F4-AC3 | One date-only occurrence interval lies fully within the saved window; another overlaps its boundary. | Check recent eligibility. | The contained interval may qualify with its precision and basis shown; the overlapping interval remains pending and is omitted from recent cards. Do not invent a precise timestamp. |

#### Feature 5 — Preserve event continuity and focus tracking

##### User Story

> In order to follow a lead over several days,
> as a daily reader,
> I want to inspect new evidence and previous judgments in an event archive.

- **Related Success Criteria:** SC4, SC6.

##### Rules

- **F5-AC1:** Keep stable event identities, linked runs/evidence versions, past judgments, open questions, and tracking state. The Agent proposes creation, links, merges, splits, and semantic corrections; the CLI validates references/versions and stores them. Similar names alone do not establish event identity. Retain an explanation for archived judgment changes.
- **F5-AC2:** On daily runs, compare new material with archived events. Follow-ups distinguish new facts, supporting evidence, contradicting evidence, still-unconfirmed questions, and no observed progress. Repeated old links or a channel failure cannot establish no real-world progress.
- **F5-AC3:** Support ordinary, active focus, and paused tracking. Attempt checks on active unresolved focus questions in every daily research run (Q82), using the selected channel constraints. Ordinary events can receive links from new findings without a promise to actively recheck all history. Pausing stops active pursuit without deleting history.
- **F5-AC4:** Merge, split, and judgment corrections keep their prior basis and event references. Do not rewrite original evidence or delivered editions. A correction records the replacement relationships so the reader can explain the change.
- **F5-AC5:** Serialize changes to the same research and protect shared archive writes across researches. Reject stale archive submissions with a reread/resubmit action; no silent overwrite. A storage interruption preserves the prior complete commit and reports the uncommitted change.
- **F5-AC6:** The reader can refer to an Event ID to ask a follow-up or choose active/paused tracking through the host Agent. A user-requested follow-up can start linked Named-Topic research using archived context and a new fixed window; it does not rewrite the old run or edition. The Agent submits tracking choices for the CLI to save.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F5-E1: Similar names | F5-AC1 | Two institutions release unrelated products both called Model Z. | Propose event links. | Agent distinguishes occurrences; naming alone does not merge them; saved references reflect that decision. |
| F5-E2: Second-day counterevidence | F5-AC1, F5-AC2 | Day 1 event EV-A includes an unverified speed claim. Day 2 independent test contradicts it. | Prepare follow-up. | Link EV-A, the new test, and changed judgment; prior claim and its original basis remain visible. |
| F5-E3: Focus and pause | F5-AC3 | EV-A active with an unanswered claim; EV-B ordinary. | Run daily research, then pause EV-A before the next run. | First run attempts a check for EV-A and saves its outcome; next run does not actively pursue paused EV-A. Both histories remain; EV-B can gain newly found links. |
| F5-E4: No new material and outage | F5-AC2 | Available sources add nothing to EV-A; X fails. | Write follow-up. | Say no new evidence was observed in checked sources and show X's gap; do not claim no progress occurred. |
| F5-E5: Wrong merge corrected | F5-AC4 | Delivered E1 links two occurrences under EV-A; Agent discovers the mistake. | Submit a split/correction. | Preserve E1 and original evidence; add revision and replacement event links that explain the correction. |
| F5-E6: Stale cross-run write | F5-AC5 | Runs R1/R2 read archive V4; R1 commits V5. | R2 submits a V4-based edit. | Reject it as stale; V5 remains unchanged; R2 must read V5 and resubmit. |
| F5-E7: Interrupted storage | F5-AC5 | A revision cannot finish because storage fills. | Save the revision. | Retain the last complete state; report failure rather than a committed partial archive. |
| F5-E8: Reader follow-up | F5-AC6 | Brief links EV-A and an unanswered speed claim; EV-A is ordinary. | Reader asks the host Agent to research the claim and track EV-A actively. | Start user-requested Named-Topic with EV-A context/new window; save active tracking. Old brief remains unchanged. |
| F5-E9: Resume focus | F5-AC3, F5-AC6 | EV-A is paused; its open claim and earlier evidence remain saved. | Reader asks the host Agent to resume focus tracking. | Save active tracking; the next daily run attempts a check on the open claim without deleting prior history. |

#### Feature 6 — Show traceable current heat

##### User Story

> In order to notice popular developments without confusing popularity with proof,
> as a daily reader,
> I want to read source heat lists with comparable observations and visible limits.

- **Related Success Criteria:** SC3, SC5.

##### Rules

- **F6-AC1:** Link each heat observation to an event, source, metric meaning, and observation time. Separate heat from research value and fact status. No cross-platform metric sum or invented growth claim is allowed. Existing event/claim qualification still applies.
- **F6-AC2:** A current heat observation must be no later than finalization and no more than 24 hours old. Exactly 24 hours satisfies freshness; more than 24 does not. It may occur after the fixed event window ends (Q83); the event/development must still meet its own eligibility rules. Stale observations cannot support current rankings.
- **F6-AC3:** In Siglens-computed groups, compare only the same platform, metric meaning, and unit (Q81). Use the maximum valid observation for the same event/metric; rank at least two comparable event samples by raw values descending. Show publication/observation times without age adjustment (Q79). Show source-provided positions separately, preserving the supplied snapshot and stated basis. Do not apply count aggregation or raw-value sorting to those positions.
- **F6-AC4:** Keep missing metrics missing; do not replace them with zero. With fewer than two comparable samples, show available data and an insufficient-sample explanation without a Siglens-computed rank. A source-provided position can be shown as the source's observation without inventing a local ranking.
- **F6-AC5:** Heat lists and follow-ups reuse event/evidence references. Repeating an event in another section does not create another topic card. Do not hide extra recent cards in heat or follow-up sections to bypass the configured maximum.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F6-E1: Different units | F6-AC1, F6-AC3 | Event A has 100 X likes; Event B has 30 HN points. | Build heat view. | Show source metrics separately; do not compute a comparable score of 130. |
| F6-E2: Freshness boundary | F6-AC2 | Eligible events; observation ages at finalization are 24h and 24h1s. | Validate heat inputs. | First satisfies freshness; second cannot support a current ranking. |
| F6-E3: First-run observation | F6-AC2 | Run created at 12:00Z with fixed event-window end 12:00Z; eligible event at 11:00Z; heat observed 12:05Z; finalization 12:10Z. | Validate heat. | Observation is eligible at age five minutes despite being after the event-window end; the event window remains unchanged. |
| F6-E4: Two samples | F6-AC3 | Two eligible events have fresh HN points 95 and 80; the first was published earlier. | Build that group. | Show 95 before 80 with publication/observation times; do not age-adjust the order. |
| F6-E5: Maximum valid value | F6-AC3 | Same event/group observations 80 and 95 valid; value 110 stale. | Aggregate that event. | Select 95; repeated observations do not count as additional event samples. |
| F6-E6: Missing sample | F6-AC4 | One event has a fresh value; a second has no metric. | Build heat view. | Show one available value and missing state; no fabricated zero or ranked list. |
| F6-E7: Heat is not eligibility | F6-AC1 | Pure launch rumor attracts many likes; official release has zero likes. | Select developments. | Exclude the rumor under F3; keep the release eligible for investigation. |
| F6-E8: Reused sections | F6-AC5 | Brief already has 21 default cards; heat and follow-up reference three of those events. | Validate count. | References do not add cards; a 22nd full recent card is still rejected regardless of section. |
| F6-E9: Provider rank | F6-AC1, F6-AC3, F6-AC4 | Saved source snapshot reports one eligible event at position 1; another feed reports likes 100/80. | Present heat. | Show position 1 as source-reported with its snapshot/basis; do not take maximum positions, mix it with likes, or invent a one-event local rank. |
| F6-E10: Different metric meanings | F6-AC3 | Same platform has cumulative likes and one-hour new likes. | Group values. | Keep these meanings in separate groups even though both count likes. |
| F6-E11: Future observation | F6-AC2 | Draft cites an observation timestamp later than finalization. | Validate heat inputs. | Reject that observation as future-dated; no valid freshness interval exists. |

#### Feature 7 — Produce a readable Briefing and final edition

##### User Story

> In order to read a useful brief and inspect its basis,
> as a daily reader,
> I want to read concise developments, follow-ups, original links, and coverage in a saved edition.

- **Related Success Criteria:** SC1, SC4, SC5, SC6.

##### Rules

- **F7-AC1:** Provide English Briefing content covering an overview, current heat, important developments, follow-ups, original sources, and coverage/limits. Keep important low-engagement developments visible independently of heat. The external Agent controls daily organization; the CLI supplies and validates research content.
- **F7-AC2:** Each final Discovery card includes the six Topic Card elements in Glossary, a window-eligible event/development, limited enrichment, and cross-channel check attempts. Validate required content, existing evidence references, recorded review/degradation, time basis, and configured count. The Agent verifies semantic support; structure validation is not proof of truth.
- **F7-AC3:** Keep structured research data/state in JSON and human research outputs in Markdown. Store evidence locally. The external workflow may distribute relevant files as attachments or with Briefing output. Preserve counterevidence and gaps when making the reading view shorter; do not impose a mandatory attachment or word limit from an unconfirmed proposal.
- **F7-AC4:** Failed delivery validation keeps the draft and lists concrete gaps without a final edition. Channel failure, legal Jev degradation, one direct source, or a Named-Topic inconclusive finding do not alone prevent a compliant edition.
- **F7-AC5:** Finalized editions are immutable. Corrections produce a new linked edition identifying what it replaces; do not overwrite the old one or its evidence references.
- **F7-AC6:** Distinguish research in progress, interruption, healthy empty output, a complete result for attempted scope, and partial coverage. Healthy no-result output reports no qualifying developments found, with checked scope. Faults never become a claim that nothing happened.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F7-E1: Continuous brief | F7-AC1, F7-AC2 | Day 1 finds EV-A release and EV-B popular debate; Day 2 gets the EV-A test in F5-E2. | Read consecutive briefs. | Day 2 links EV-A and explains the changed speed claim, shows heat separately, and retains source/coverage information. |
| F7-E2: Local evidence | F7-AC3 | Many source extracts and one material counterexample accompany four cards. | Make a shorter reading view. | Save full acquired text locally, JSON state and Markdown output; keep counterexample/gaps in the brief and link detailed evidence. External attachment delivery is optional. |
| F7-E3: Invalid citation | F7-AC2, F7-AC4 | Draft cites absent evidence ID EV999. | Validate/finalize. | Keep draft, report that reference, create no final edition. |
| F7-E4: Invalid recent card | F7-AC2, F7-AC4 | Card lacks time basis or Discovery review/degradation; another draft contains 22 cards at default limit. | Validate each draft. | Report each missing prerequisite or excess count; preserve drafts and prior editions. |
| F7-E5: Partial but valid | F7-AC4, F7-AC6 | Reddit failed; remaining evidence supports release; Jev timeout recorded; required fields/check attempts present. | Finalize. | Allow an edition with explicit channel and review gaps; it is not complete channel coverage. |
| F7-E6: Healthy empty | F7-AC6 | All selected ready queries succeeded; no qualifying recent event; no unresolved request failure. | Prepare daily output. | Save a concise no-qualifying-results statement with scope/coverage; do not invent cards or imply all-world absence. |
| F7-E7: Interrupted collection | F7-AC6 | Run stops during collection. | Show status. | Identify incomplete research and recovery action; do not label it a formal daily brief. |
| F7-E8: Edition correction | F7-AC5 | E1 is finalized; a cited claim needs correction. | Finalize corrected E2. | Preserve E1; E2 links E1 as replaced and explains the change. |

#### Feature 8 — Resume research and operate it through an Agent guide

##### User Story

> In order to continue work without losing results or guessing interfaces,
> as a host Agent operator,
> I want to use an independent CLI with saved progress, clear responses, and an operation guide.

- **Related Success Criteria:** SC6, SC8.

##### Rules

- **F8-AC1:** Provide the standalone Python 3.12+ CLI with `uv tool` installation and built-in Agent guidance on capabilities, prerequisites, input/output examples, errors, and continuation. Support local research without Multica; public package release is deferred.
- **F8-AC2:** Default CLI responses to JSON. Keep diagnostic/progress logs separate from response data. Distinguish operation completion, coverage completeness, research sufficiency, finalization, and delivery. Errors state the problem, known cause or unknown cause, and next action.
- **F8-AC3:** Repeating the same research operation reuses saved successful results, including healthy empty results. After interruption, continue only failed or unfinished parts. Request successful operations again only on explicit refresh; refresh preserves the window.
- **F8-AC4:** Preserve intermediate evidence and state during interruptions. Record an uncertain upstream request outcome when its response was not saved; do not claim guaranteed single execution or invent exact hidden Grok request counts.
- **F8-AC5:** Allow paid access without collection-count or Jev-cost quotas. Handle service limits with bounded requests/retries and retained failure state; removing a research budget does not require endless retries. CLI does not schedule Agents, upgrade models, transport research, or initiate another research round.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F8-E1: Independent use | F8-AC1 | Clean Python 3.12+ environment; Multica absent. | Install locally through uv tool and read guide. | Agent can inspect supported plans and run both research entrypoints; Multica absence does not block research. |
| F8-E2: Structured response | F8-AC2 | Collection completes with one channel failure and report still a draft. | Read JSON output. | Operation completion, partial coverage, and draft state are distinguishable; logs do not corrupt JSON. |
| F8-E3: Partial resume | F8-AC3 | Plan has five successes, one failure, one unfinished operation. | Resume same plan. | Reuse five successes; continue the other two without refreshing the five. |
| F8-E4: Empty cache | F8-AC3 | HN query succeeded with no results. | Repeat the operation, then explicitly refresh. | First reuses empty success; explicit refresh requests again with unchanged window. |
| F8-E5: Lost model response | F8-AC4 | Model may have processed a call; connection closes before saving response. | Recover. | Record uncertain execution; do not claim retry cannot incur another call or cost. |
| F8-E6: Rate limit | F8-AC2, F8-AC5 | Upstream returns a rate limit and retry guidance. | Execute plan. | Use bounded retry respecting guidance; retain failure/continuation information if unresolved; no invented budget-exhausted state. |
| F8-E7: Handoff elsewhere | F8-AC5 | Successor Agent runs in a different machine/worktree. | Continue through Skill workflow. | External tools make evidence accessible; CLI does not pretend a local absolute path transports it. |

#### Feature 9 — Deliver and reconcile through the external workflow

##### User Story

> In order to receive one reliable daily brief,
> as a Multica reader,
> I want to receive a brief with confirmed delivery and explicit handling of uncertain outcomes.

- **Related Success Criteria:** SC7.

##### Rules

- **F9-AC1:** The external workflow chooses schedule/timezone, daily issue organization, and configured target, then sends via Multica CLI. The research CLI grants an exclusive local delivery claim and returns the immutable edition and payload/attachment hashes. Network publication and transport remain external.
- **F9-AC2:** Before sending, verify target/readiness and claim ownership. Invalid target, missing authorization, or a competing local claim cannot trigger a send. Preserve the ready edition and return a correction action.
- **F9-AC3:** Record returned receipts separately from research finalization. A successful finalized edition is not a confirmed delivery. After confirmed delivery for the same edition/target, a retry does not publish it again.
- **F9-AC4:** A known unsent failure allows retry. A lost response or uncertain outcome enters unknown and requires external reconciliation before retry. Proven delivered confirms the record; proven unsent permits retry; unresolved outcome stays unknown and requests external/manual action.
- **F9-AC5:** Local exclusivity cannot coordinate independently copied ledgers on different machines. External orchestration must keep delivery ownership serial across runners and transfer the required records/content; do not promise exactly-once transport from a local lock alone.

##### Key Examples

| Example | Related Rule | Given: Context / Input | When: Action / Event | Then: Expected Outcome |
|-----|-----|-----|-----|-----|
| F9-E1: Normal delivery | F9-AC1, F9-AC3 | E1 ready; valid target; external daily workflow configured. | Claim, publish externally, return receipt. | CLI grants claim/data without network posting; workflow sends; receipt marks E1/target delivered. |
| F9-E2: Invalid target | F9-AC2 | E1 ready; target absent or not authorized. | Request send. | No network publication; retain E1 and report target repair. |
| F9-E3: Competing claims | F9-AC2 | Two local tasks request E1 for the same target. | Claim delivery. | Only one gets permission; the other reads the existing status without sending. |
| F9-E4: Duplicate retry | F9-AC3 | E1/target already has confirmed receipt. | Repeat delivery request. | Return confirmed status; do not post again. |
| F9-E5: Known unsent | F9-AC4 | External pre-send connection failure proves no message was sent. | Record failure and retry. | Preserve edition and allow another owned send attempt. |
| F9-E6: Response lost | F9-AC4 | Post may have succeeded; reply was lost. | Resume workflow. | Mark unknown, reconcile externally, and prohibit blind repost. |
| F9-E7: Reconciliation outcomes | F9-AC4 | Unknown delivery; external check proves delivered, proves unsent, or remains inconclusive. | Submit reconciliation. | Confirm delivery, allow retry, or retain unknown with external/manual follow-up respectively. |
| F9-E8: Two machine copies | F9-AC5 | Two runners have copied local ledgers. | Schedule E1 delivery. | External workflow maintains one owner; independent local claims cannot establish global exclusivity. |
