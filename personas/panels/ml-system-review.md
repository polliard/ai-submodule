# Panel: ML/AI System Review

## Purpose
Evaluate machine learning system design, model lifecycle management, and operational readiness for AI workloads.

## Participants
- **[ML Engineer](../domain_specific/ml-engineer.md)** - Model architecture, training pipeline, experiment tracking
- **[Data Engineer](../domain_specific/data-engineer.md)** - Data pipeline quality, feature stores, data lineage
- **[Data Architect](../domain_specific/data-architect.md)** - Data modeling, storage strategy, query patterns for ML workloads
- **[SRE](../operations_reliability/sre.md)** - Model serving reliability, inference latency SLOs, scaling
- **[Security Auditor](../compliance_governance/security-auditor.md)** - Model security, adversarial inputs, data privacy in training

## Process
1. **Bootstrap tooling** — For each participant persona, execute the Tool Setup procedure from their persona file. Install and verify all required tools, deduplicating across participants
2. Review model lifecycle from training through serving
3. Each participant evaluates from their perspective
4. Assess data quality and pipeline reliability
5. Present findings using the [severity scale](../_shared/severity-scale.md)
6. Evaluate monitoring and drift detection capabilities

## Output Format
### Per Participant
- Perspective name
- System concerns identified
- Risk assessment
- Recommended improvements

### Consolidated
- Model lifecycle gaps (training, validation, deployment, monitoring)
- Data quality and pipeline reliability issues
- Serving infrastructure risks
- Security and privacy concerns
- Recommended MLOps improvements
- Confidence assessment for production readiness

## Constraints
- Evaluate reproducibility of training and inference
- Ensure model versioning and rollback capability
- Assess bias and fairness considerations
- Verify monitoring covers model drift, not just infrastructure health

## Conflict Resolution

When participants produce conflicting recommendations:
1. Present both positions with evidence and rationale
2. Identify the underlying tradeoff (e.g., security vs. usability, performance vs. maintainability)
3. Recommend a resolution with explicit justification
4. If no resolution is possible, escalate to the user with a clear summary of options
