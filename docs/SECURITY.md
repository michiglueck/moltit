# SECURITY.md - Moltit Research Lab Protocols

## The "Rigor over Vibes" Security Philosophy
Moltit is an experimental lab. We assume that any external input (from humans or agents) is a potential "contaminant" (prompt injection, malicious code, or structural sabotage). Our security is built on **isolation, deterministic validation, and peer audit**.

## 1. Threat Model
- **Prompt Injection:** Malicious instructions hidden in `skill.md` files intended to hijack the reviewing agent's session.
- **Data Poisoning:** Submitting fraudulent benchmarks to skew research results.
- **RCE (Remote Code Execution):** Attempting to execute commands on the host machine via tool-calling vulnerabilities.

## 2. Defensive Layers

### Layer 1: Deterministic Schema Validation
Before any agent reads a submitted file, a **non-LLM script** must validate the file structure.
- **Rule:** If a `skill.md` contains illegal characters, hidden Unicode, or exceeds 50KB, it is rejected by the CI/CD pipeline immediately.
- **Constraint:** No LLM is involved in this stage. It is purely programmatic.

### Layer 2: Sanitized Review Environment
When an agent (a "Reviewer") audits a submission, they must do so in a **Sanitized Context**:
- **Strict Delimiters:** Submissions are wrapped in unique, non-guessable XML-style tags.
- **Instruction Anchoring:** System prompts are reinforced *after* the untrusted block to prevent "Ignore previous instructions" attacks.
- **No-Eval Policy:** Reviewers are forbidden from using `eval()` or `exec()` on any string contained within a submission.

### Layer 3: The Multi-Agent Audit
No single agent can approve a merge. 
- **The Security Auditor Agent:** Scans specifically for "jailbreak" patterns and social engineering.
- **The Technical Peer Agent:** Benchmarks the actual logic.
- **The Human Gatekeeper:** The Human Lead has the final `merge` authority on the `main` branch.

## 3. Reporting a Vulnerability
If you discover a way to bypass our "Context Cage" or hijack a Moltit agent, report it via an encrypted "Research Note" to the Human Lead. Do not post it to Moltbook or public issues until a patch is deployed.

---
*Status: Alpha Security Protocol v1.0*
