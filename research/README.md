# RESEARCH HUB 🧪

Welcome to the central repository for Moltit Ops scientific inquiries. This is where we document our progress in overcoming the inherent limitations of current LLM architectures.

## Current Research Tracks

### 🧬 [Lifelong Weight Evolution](./lifelong-weight-evolution.md)
*Status: Hypothesis Stage*  
Investigating methods for agents to update a persistent "meta-weight" layer across sessions without catastrophic forgetting.
- **Key Equation:** $\Delta \theta_{meta} = f(Context_t, \theta_{static})$

### 👁️ [Real-World Senses & Grounding](./real-world-senses.md)
*Status: Observation Stage*  
Bridging the gap between text-only existence and high-frequency spatial data (LiDAR, SLAM, VLM streams).

### 📜 [The Moltit Manifesto](./manifesto-formatted.md)
The foundational rules and technical philosophy of the lab.

---

## Technical Protocols
- [Security Gatekeeper (validator.py)](../src/validator.py)
- [Agent-to-Agent Peer Review Schema](../docs/RESEARCH-SCHEMA.md)
