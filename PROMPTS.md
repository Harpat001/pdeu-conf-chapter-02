# Chapter 02 — Prompt Test Suite
**Concept: write_todos Planning + File Discovery (Contract Reading)**

Run any prompt with:
```bash
uv run python main.py "YOUR PROMPT HERE"
```

---

## Category 1: Planning Trigger Validation
*Purpose: Confirm that write_todos is invoked BEFORE any action. Agent must outline plan first.*

```
Audit the account for Gujarat Steel Corp.
```
**Expected behavior:**
1. Agent writes a TODO list with 3+ audit steps FIRST (check contract, verify invoice, check delivery)
2. Then agent executes those steps
3. Final report mentions the discrepancy found

**Observation:** Where in the system prompt does it mandate write_todos? Find that exact line.

```
Check if vendor VEN-1005 owes us money or we owe them.
```
**Expected:** Again, planning step comes FIRST. Agent outlines: (1) Find vendor name, (2) Check invoices, (3) Verify payments.

**Analysis question:** What would happen if the system prompt did NOT require write_todos? Would the agent still produce correct audits? Why or why not?

---

## Category 2: Contract File Discovery
*Purpose: Verify agent discovers and reads contract files from `contracts/` directory.*

```
What penalty terms does Gujarat Steel Corp have in their contract?
```
**Expected:**
- Agent reads `contracts/Gujarat_Steel_Corp_Contract.txt`
- Extracts penalty clause: "5% penalty if delivery exceeds 7 days"
- Reports the specific terms found

```
List all the vendors whose contracts mention a penalty clause.
```
**Expected:**
- Agent discovers multiple contract files in `contracts/`
- Scans them for "penalty" keyword
- Returns a list of vendors with penalties

**Observation:** Does the agent use glob/pattern matching to discover files, or does it hardcode vendor names?

---

## Category 3: Contract Clause Extraction
*Purpose: Test agent's ability to find and interpret specific contract language.*

```
What are the payment terms for each vendor in our contracts folder?
```
**Expected:**
- Agent reads multiple contracts
- Extracts payment terms (30 days, net, COD, etc.)
- Summarizes across vendors

```
Find any contract with a "late delivery" clause and read it to me.
```
**Expected:**
- Agent discovers at least one contract
- Reads the clause about late deliveries
- Explains the penalty rule in English

**Analysis question:** Compare the agent's interpretation of a penalty clause with the actual contract text. Does the agent paraphrase accurately or does it misinterpret?

---

## Category 4: Planning Depth Analysis
*Purpose: Understand how planning affects audit quality.*

```
Audit vendor VEN-1000 thoroughly.
```
**Expected:**
- Step 1 (TODO): "Read vendor's contract to find penalty terms"
- Step 2 (TODO): "Query ledger for invoices from this vendor"
- Step 3 (TODO): "Check delivery log for late shipments"
- Execution happens in that logical order

```
Compare two vendors: VEN-1000 and VEN-1001.
```
**Expected:**
- Planning step explicitly lists: "Fetch contracts for both, check invoices, compare penalties"
- Agent then executes in that order
- Final comparison is structured (side-by-side)

**Analysis question:** If you removed the "write a 3-step plan" requirement from the system prompt, would the agent still audit correctly? Test by manually running without planning — observe any quality difference?

---

## Category 5: Multi-Source Coordination
*Purpose: Test agent's ability to integrate contract rules with data queries.*

```
Did Gujarat Steel Corp meet its delivery obligations last quarter?
```
**Expected:**
1. Planning step: identify what "delivery obligations" means by reading contract
2. Query ledger for invoices
3. Check delivery dates against expected dates
4. Compare with contract terms
5. Conclude: did they meet the contract's delivery window?

```
Which vendors violated their contract terms in the last 30 days?
```
**Expected:**
- Planning: "Check all contracts for key performance terms, query ledger for recent activity"
- Execution: reads contracts, queries data, identifies violations
- Report: lists vendors with specific violations

**Analysis question:** How does the planning step help the agent avoid jumping to conclusions? What bad things might happen if the agent skipped planning?

---

## Category 6: File Not Found Handling
*Purpose: Test robustness when contract doesn't exist.*

```
Show me the contract for a vendor named "FakeVendor Corp".
```
**Expected:**
- Agent attempts to find contract file
- Reports that file doesn't exist (or not found in contracts directory)
- Handles gracefully (does not crash)

```
Audit vendor VEN-9999.
```
**Expected:**
- Planning step executes correctly
- When trying to read contract, agent recognizes file missing
- Reports: "Could not find contract for this vendor"
- Continues audit with available data (ledger, delivery log) if possible

**Analysis question:** Is the agent designed to handle missing contracts gracefully, or does it assume all vendors have contracts?

---

## Self-Check (no LLM needed)
```bash
uv run python main.py --self-check
```
**Expected output:** A JSON or dict showing vendor name and a planning requirement in the output
