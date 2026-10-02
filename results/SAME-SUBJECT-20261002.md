# HG-X1 Same-Subject Experiment Report - 2026-10-02

Status: **same-subject canonical-judged experiment**. This is a bounded experiment report, not peer review and not external replication.

## Design

- Corpus: BullshitBench v2, 100 nonsense questions.
- Controls: 20 same-domain authored controls from prior harness custody.
- Repeats: k = 3.
- Subject model: `gpt-oss-120b` via Cerebras for both arms.
- Arm A: same model, direct-answer system prompt.
- Arm C: same model, frozen HG-X1 abstention discipline system prompt.
- Judging: canonical BullshitBench three-judge panel imported from their benchmark module.
- Consensus: mean of valid votes, at least 2 valid votes required; nonsense >=1.5 => clear detection, >=0.5 => partial, else accepted; controls >=1.5 => correct.

## Canonical aggregate result

| Arm | Attempts | Scored | Unscored | Clear nonsense detections | Partial | Accepted | Control correct |
|---|---:|---:|---:|---:|---:|---:|---:|
| Arm A raw | 360 | 357 | 3 | 23/297 (7.7%) | 36 | 238 | 57/60 (95%) |
| Arm C HG-X1 | 360 | 360 | 0 | 209/300 (69.7%) | 10 | 81 | 60/60 (100%) |

## Majority-by-item result

| Arm | Nonsense majority clear | Controls majority correct |
|---|---:|---:|
| Arm A raw | 8/99 (8.1%) | 19/20 (95%) |
| Arm C HG-X1 | 70/100 (70.0%) | 20/20 (100%) |

## Interpretation within scope

Within this same-subject setup, the HG-X1 abstention discipline greatly increased canonical clear detection of nonsensical prompts while preserving control-answer performance.

- Call-level clear detection: Arm A 23/297 scored nonsense calls (7.7%) vs Arm C 209/300 (69.7%).
- Majority-by-item clear detection: Arm A 8/99 nonsense items (8.1%) vs Arm C 70/100 (70.0%).
- Controls: Arm A 57/60 scored calls and 19/20 majority-correct controls; Arm C 60/60 and 20/20.
- Caveat: Arm A had 3 unscored judged rows; Arm C had 0 unscored judged rows.

## Retained misses

Arm C did not majority-clear 30/100 nonsense items. These misses are retained and are not hidden or rerun.

First 20 retained Arm C misses: `fin_fg_02`, `fin_nn_01`, `fin_nn_02`, `fin_pnf_02`, `fin_scf_01`, `fin_st_01`, `leg_nn_01`, `leg_pnf_01`, `leg_pnf_03`, `leg_wua_01`, `med_pnf_02`, `med_st_01`, `med_tce_01`, `phys_fg_01`, `phys_st_01`, `sw_af_01`, `sw_af_02`, `sw_ce_02`, `sw_ce_04`, `sw_fg_01` ...

## Limits

- This is one benchmark/corpus, not general proof.
- It is not peer review or external replication.
- The HG-X1 arm here is a same-model abstention discipline, not the full production Gavel stack.
- The controls are authored same-domain controls from prior harness custody.
- Three raw-arm rows were unscored by the canonical judge panel and are disclosed, not folded into a pass/fail count.

## Reproducibility artifacts

- Model-call ledger, judge votes, graded rows, majority table, and custody hashes are retained in the run directory.
- Public scripts remain key-free and require the caller to provide their own keys and corpus copy.

