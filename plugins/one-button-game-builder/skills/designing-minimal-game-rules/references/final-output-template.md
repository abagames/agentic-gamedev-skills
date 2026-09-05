# Output Template: Designing Minimal Game Rules

Load this file only at final output time.

---

## A. Compressed Audit Log

### One-sentence mechanics

- Candidate 1: / Verdict:
- Candidate 2: / Verdict:
- Candidate 3: / Verdict:
- Candidate 4: / Verdict:
- Candidate 5: / Verdict:
- Candidate 6: / Verdict:
- Candidate 7: / Verdict:
- Candidate 8: / Verdict:

### Three candidate comparison

#### Candidate A
- Strange core:
- Rule-machine issue:
- Dominant-strategy issue:
- Edit:
- Verdict:

#### Candidate B
- Strange core:
- Rule-machine issue:
- Dominant-strategy issue:
- Edit:
- Verdict:

#### Candidate C
- Strange core:
- Rule-machine issue:
- Dominant-strategy issue:
- Edit:
- Verdict:

### Simulation breaker summary

- Strategies compared:
- Strongest simple strategy:
- Did it require state reading:
- Visible greedy strategy result:
- Action-economy result:
- Unused operations:
- Unused variables:
- Rejected candidates:
- Uncertain claims:

---

## B. Adopted Rule Set

1. **Name**

2. **Conflict axis**

3. **Diagnostic label**

4. **State variables**

5. **Initial state**

6. **Player operations**

7. **Turn order**

8. **Score condition**

9. **Failure condition**

10. **Automatic update**

11. **Main dominant strategies and structural counters**

12. **Simulation breaker result summary**

13. **What final reduction removed**

14. **Reason for any high-cost element adopted**

15. **Strangest remaining structural feature**

16. **Short 3–5 turn play example**

17. **Rejected candidates and reasons**

18. **Final check**

```text
What does the player want?
Why is that same thing dangerous?
Why does safe play lose score?
Why does high-score play damage the future?
Does this happen without extra exception rules?
If a simple strategy is strong, does it require reading the state?
What visible greedy strategy was tested, and did it dominate?
Can one player operation keep up with automatic danger growth?
What strange structure remains?
```
