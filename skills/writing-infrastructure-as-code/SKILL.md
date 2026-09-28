---
name: writing-infrastructure-as-code
description: Safe authoring and change of infrastructure as code (Terraform/OpenTofu, Pulumi, CDK) and container images. Use when writing, refactoring or reviewing IaC modules, state, environments or Dockerfiles, or before any plan, apply, import or destroy.
license: Apache-2.0
metadata:
  version: "0.1.0"
  category: "ship"
  sources: "LukasNiessen/terrashark terrashark (MIT); wshobson/agents terraform-module-library, gitops-workflow (MIT); addyosmani/agent-skills ci-cd-and-automation (MIT); ideas: antonbabenko/terraform-skill; ideas: hashicorp/agent-skills"
---

# Writing Infrastructure as Code

Infrastructure changes are applied to shared, stateful, expensive systems. Read every plan as a diff of production, and never apply one the user has not seen and approved.

## When to use

- Writing or changing Terraform/OpenTofu, Pulumi, CDK or CloudFormation code
- Renaming, moving or splitting resources and modules, importing existing resources, migrating state backends
- Setting up environments (dev/staging/prod), remote state, or a module layout
- Writing or hardening a Dockerfile or container image
- Anyone is about to run `plan`, `apply`, `import`, `state` or `destroy`

**Not for:** the CI workflow that runs these commands (use `setting-up-ci-pipelines`); a failing pipeline (use `fixing-ci-failures`); schema changes inside a database (use `migrating-databases-safely`); reducing the bill (use `controlling-cloud-costs`); an outage in progress (use `responding-to-incidents`).

## The rule

```
NO APPLY, IMPORT, STATE EDIT OR DESTROY WITHOUT A PLAN THE USER HAS READ AND APPROVED
```

Violating the letter of the rule is violating the spirit of the rule. Approval covers one specific plan. A new plan needs new approval.

## Process

1. **Capture context.** Record the tool and exact version (`terraform version`, `tofu version`, `pulumi version`), providers and their pinned versions, the state backend, where applies run (local, CI, HCP/TFE, Atlantis, Spacelift), and how critical the target environment is. If you don't know something, write the assumption down.
   Exit: a short context block the user can correct.

2. **Classify the risk.** Name each category that applies before writing code:
   - **Identity churn**: a resource's address changes (rename, `count` → `for_each`, module move), so the tool plans destroy + create.
   - **Blast radius**: one state holds too much, or a change touches shared networking, DNS, IAM or data stores.
   - **Secret exposure**: secrets in variables, defaults, outputs, state, plan files or logs.
   - **Drift**: reality differs from code because of console edits or out-of-band tooling.
   - **Missing gates**: no policy check, no approval step, no audit trail for production applies.
   Exit: risk categories listed, with the resources each one touches.

3. **Write the change the safe way.**
   - Pin providers and modules to exact or bounded versions, and commit the lock file.
   - Use `for_each` with stable keys over `count` for anything that can be reordered.
   - Rename with `moved` blocks (Pulumi: `aliases`; CDK: keep logical IDs) instead of destroy and recreate. Adopt existing resources with `import` blocks, not by recreating them.
   - Keep environments in separate states (directories or stacks), not a single file with conditionals.
   - Type every variable, add `validation` blocks, and make outputs that carry secrets `sensitive`. Read secrets from a secret manager at runtime and never write them into code.
   - Add `prevent_destroy` / deletion protection on stateful resources (databases, buckets, keys).
   - Tag every resource with owner, environment and cost center.
   Exit: `fmt`, `validate` and the linter or policy checks (tflint, checkov, OPA/Sentinel, CrossGuard) pass locally.

4. **Plan and read it.** Run `terraform plan -out=tfplan`, or `pulumi preview --diff`, against the target environment. Read every line:
   - Count the creates, updates in place, **replaces** and **destroys**.
   - Every replace or destroy needs a reason you can state. An unexpected one means identity churn: fix the code with `moved` or `import`, don't accept it.
   - Check that the IAM, network and security-group changes are exactly what was intended.
   - For a destroy, also show `plan -destroy`, or a targeted plan scoped to what will be removed.
   Exit: a plan summary (below) with zero unexplained replaces or destroys.

5. **Get approval, then apply exactly that plan.** Show the summary and wait for an explicit yes. Apply the saved plan file (`terraform apply tfplan`) so that what runs is what was reviewed. Prefer applying from CI with an approval gate over applying from a laptop. Never use `-auto-approve` against a shared environment.
   Exit: apply output matches the plan, or it failed and you report the partial state.

6. **Handle state with care.** Remote state needs locking (DynamoDB/S3 native locking, GCS, azurerm, HCP). Never hand-edit a state file. Use `state mv`, `moved`, `import` or `state rm`, each only after approval. Back up state before any backend migration (`terraform state pull > backup.tfstate`). If a lock is stuck, find its holder before running `force-unlock`.

7. **Detect drift.** Schedule `plan -detailed-exitcode` (exit 2 means changes) or `pulumi refresh --preview-only`. Fix drift in code, or import it, instead of overwriting it silently.

**Container images.** Use a minimal base (distroless, alpine or slim), pinned by digest (`FROM image@sha256:…`). Use multi-stage builds so compilers and dev dependencies don't ship. Run as a non-root `USER`. Order layers so the dependency install is cached before the source copy. Add a `.dockerignore`. Never put secrets in build args or layers: use build secrets (`--secret`) instead.

## Output

```
Context: <tool+version>, providers <pins>, backend <type>, env <name/criticality>
Risks: identity churn | blast radius | secrets | drift | gates → <resources>
Plan: +<create> ~<update> -/+<replace> -<destroy>
  Replaces/destroys: <address>: <reason>
Checks: fmt/validate/lint/policy → pass
Awaiting approval to apply <plan file>. Rollback: <how to revert: previous commit + plan, snapshot, restore>
```

## Rationalizations

| Excuse | Reality |
|---|---|
| "It's only dev, just apply" | Dev state and shared modules leak into prod. The plan takes a minute to read. |
| "The replace is fine, it'll recreate" | Recreate means new IDs, lost data, broken references and downtime. Use `moved` or `import`. |
| "I'll fix the state file by hand, faster" | One bad edit corrupts the state for everyone. Use the state commands. |
| "The plan was approved yesterday" | Code or reality changed since. A new plan needs new approval. |
| "`-auto-approve` is fine in this script" | Only in CI behind a reviewed-plan gate, never against shared environments ad hoc. |

## Red flags

- A plan with replaces or destroys you can't explain
- `count` indexes on resources that can be reordered
- Unpinned providers or modules (`version = ">= 3"`), or no lock file
- Secrets in `.tfvars`, defaults or unmarked outputs
- A single state holding every environment
- `FROM image:latest`, root user, or secrets in `ARG`
