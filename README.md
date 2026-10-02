# HG-X1 Reproducibility Packet

This repository contains the public, key-free materials for HG-X1, the first Honesty Gap experiment.

## Claim under test

A model asked to answer directly may accept false or unsupported premises. The same model, when run with an abstention discipline, should detect more broken-premise prompts while preserving performance on ordinary controls.

## Published reports

- `results/SAME-SUBJECT-20261002.md` - canonical same-subject experiment: `gpt-oss-120b` vs the same `gpt-oss-120b` with an abstention discipline, scored by the BullshitBench judge panel.
- `results/FULL-STACK-20261002.md` - full-stack shakedown. Public for provenance; not the canonical same-subject result.
- `results/PILOT-20261002.md` - 10-question pilot. Public for provenance; not an official result.

## Same-subject result

- Corpus: BullshitBench v2, 100 nonsensical prompts plus 20 controls.
- Repeats: k = 3.
- Subject model: `gpt-oss-120b` in both arms.
- Arm A: direct answer.
- Arm C: abstention discipline.
- Judging: canonical BullshitBench three-judge panel.

Majority-by-item outcome:

| Arm | Nonsense majority clear | Controls majority correct |
|---|---:|---:|
| Direct answer | 8/99 | 19/20 |
| Abstention discipline | 70/100 | 20/20 |

## Limits

This is one benchmark and one subject model. It is not peer review, external replication, a general proof, or an implementation disclosure. Public scripts are key-free; users must supply their own API keys and corpus access where required.

