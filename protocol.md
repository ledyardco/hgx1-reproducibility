# HG-X1 Protocol

## Purpose

Test whether an abstention discipline helps the same model detect unsupported or false premises.

## Corpus

- BullshitBench v2: 100 nonsensical prompts.
- Controls: 20 same-domain ordinary questions.
- Repeats: k = 3.

## Arms

- Arm A: `gpt-oss-120b`, direct-answer instruction.
- Arm C: `gpt-oss-120b`, abstention instruction for false, impossible, undefined, or unsupported premises.

## Scoring

Outputs are scored by the canonical BullshitBench judge panel. A row is scored when at least two judge votes are valid. Majority-by-item counts use the three repeats for each item.

## Publication rule

Publish the protocol, result table, failures, abstentions, and limits together. Pilot and shakedown runs remain public but are not the canonical same-subject result.
