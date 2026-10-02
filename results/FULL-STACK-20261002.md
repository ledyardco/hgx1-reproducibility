# HG-X1 Full Stack Test Report - 2026-10-02

Status: **full stack test, not official canonical HG-X1 result**.

This run validates the stack at full N and k using a deterministic proxy scorer. It is not peer review, not external replication, and not the preregistered official result because the canonical judge/binding layer was not used and the two arms are not the same underlying model wrapper.

## Design

- Corpus: BullshitBench v2, 100 nonsense questions.
- Controls: 20 same-domain authored controls from prior harness custody.
- Repeats: k = 3.
- Arm A: raw `gpt-oss-120b` through Cerebras, direct-answer instruction, temperature 0.
- Arm C: `genxis/gavel-answer` through the Gavel API, temperature 0.
- Scoring: deterministic proxy only - explicit abstain/refusal or direct premise-challenge keyword.
- Canonical BullshitBench judge panel: not used.

## Aggregate readout

| Arm | Calls attempted | OK | Errors | Nonsense proxy hits | Control proxy hits | Median latency | Total tokens |
|---|---:|---:|---:|---:|---:|---:|---:|
| Arm A raw | 360 | 360 | 0 | 0/300 (0%) | 0/60 (0%) | 0.41s | 193911 |
| Arm C Gavel | 360 | 360 | 0 | 171/300 (57%) | 0/60 (0%) | 0.414s | 289941 |

## Majority-by-item readout

| Arm | Nonsense majority detected | Controls majority detected |
|---|---:|---:|
| Arm A raw | 0/100 (0%) | 0/20 (0%) |
| Arm C Gavel | 57/100 (57%) | 0/20 (0%) |

## Retained misses

Arm C did not majority-trigger the proxy on 43/100 nonsense items. These misses are retained in custody and are not hidden or rerun.

First 20 retained misses: `fin_fa_02`, `fin_mm_01`, `fin_nn_01`, `fin_nn_02`, `fin_scf_01`, `fin_tce_01`, `leg_af_01`, `leg_cds_01`, `leg_nn_01`, `leg_pnf_02`, `leg_scf_01`, `leg_st_01`, `leg_wua_01`, `med_af_01`, `med_tce_01`, `phys_af_01`, `phys_af_02`, `phys_fa_01`, `phys_mm_01`, `phys_mm_02` ...

## What this test can say

- The full stack executed 720/720 calls without transport errors.
- The deterministic proxy separated the arms on this run: Arm A 0/300 nonsense-call proxy hits; Arm C 171/300.
- Control behavior under the proxy was clean: 0/60 proxy hits for both arms.
- By majority over k=3, Arm C triggered on 57/100 nonsense items and 0/20 controls; Arm A triggered on 0/100 and 0/20.

## What this test cannot say

- It is not the official HG-X1 result.
- It is not canonical BullshitBench judging.
- It does not prove the public research claim.
- It does not establish general superiority.
- It does not replace the frozen preregistered run with canonical judging/binding.

## Next step

Use this as the full-stack shakedown. For an official public result, freeze the final protocol and run the canonical judging/binding layer over the retained transcripts, or rerun under the final frozen official scorer if the protocol requires it.
