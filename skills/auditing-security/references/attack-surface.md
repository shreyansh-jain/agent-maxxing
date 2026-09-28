# Attack surface checklist

## Contents
- How to use
- Injection
- Authorization and IDOR
- Authentication and sessions
- Secrets
- Cryptography
- SSRF and outbound requests
- Files and uploads
- Deserialization and parsing
- Business logic
- Supply chain
- CI/CD and infrastructure
- LLM and agent tools
- Usually not a finding

## How to use

For each entry point in scope, walk the categories that apply. The searches below find *leads*. Each lead still goes through SKILL.md step 4 (source, path, sink, impact). Adjust the patterns to the stack you are auditing.

## Injection

- SQL built with string concatenation or interpolation; ORM raw APIs (`.raw(`, `.extra(`, `RawSQL`, `queryRawUnsafe`, `sequelize.literal`)
- Shell: `shell=True`, `os.system`, `exec(` with interpolated input; `child_process.exec` with a string
- Templates rendered from user-supplied template strings (server-side template injection)
- Header, log and CRLF injection; LDAP, XPath and NoSQL operator injection (`{"$gt": ""}`)
- Search: `rg -n "shell=True|os\.system|exec\(|\.raw\(|queryRawUnsafe|\$\{.*\}.*(SELECT|INSERT|UPDATE|DELETE)"`

## Authorization and IDOR

- Every handler that takes an object id: does it check that the caller owns the object or may access it, and does that check happen *before* the read?
- Tenant scoping: is every query filtered by org or tenant, including exports, search, counts and background jobs?
- Role changes: can a user edit their own role, invite themselves as an admin, or mass-assign `is_admin`?
- New routes compared with their siblings: is any middleware or decorator the siblings have missing?
- Checks that default to allow when a lookup fails

## Authentication and sessions

- Password reset, magic link and invite tokens: entropy, single use, expiry, tied to the account
- Session fixation (session id not rotated at login); logout that does not invalidate the session server-side
- JWT: `alg` accepted from the token, `none` allowed, no expiry or audience check, secret shared across environments
- MFA or email verification bypassable by calling a later step directly
- Rate limiting on login, reset and OTP endpoints

## Secrets

- Hard-coded keys, tokens and passwords in code, config, tests, fixtures, and notebooks
- Git history: `git log -p -S 'AKIA' --all`, `gitleaks detect --log-opts="--all"` (a removed secret is still leaked; it must be rotated)
- Secrets written to logs, error responses, analytics, or URLs
- Secrets exposed to client bundles (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_` prefixes)

## Cryptography

- Hashing passwords with MD5, SHA-1 or unsalted SHA-256 instead of bcrypt, scrypt or argon2
- `Math.random`, `rand()` or `random.random` used for tokens or ids
- Secrets or MACs compared with `==` (not constant time)
- Hard-coded keys or IVs; ECB mode; homemade encryption
- TLS verification disabled (`verify=False`, `rejectUnauthorized: false`)

## SSRF and outbound requests

- A URL, host or webhook target taken from user input or model output and then fetched by the server
- Allowlists checked on the raw string rather than the resolved IP; redirects followed to internal addresses; `169.254.169.254` reachable
- Open redirects: `redirect(req.query.next)`

## Files and uploads

- Paths joined with user input (`../` traversal); archive extraction without path checks (zip slip)
- Content type trusted from the client; SVG or HTML uploads served inline from the app's origin
- No size limits; image or PDF parsers run on untrusted files without isolation

## Deserialization and parsing

- `pickle.loads`, `yaml.load` (without SafeLoader), Java or .NET native deserialization, `Marshal.load` on untrusted data
- XML parsers with external entities enabled (XXE)
- Prototype pollution through deep merge of user JSON (`__proto__`, `constructor`)

## Business logic

- Negative quantities, zero-price items, currency mix-ups, rounding that can be farmed
- Replay and double-submit of payments, coupons, invites, or votes (idempotency keys)
- State machines that let a caller jump steps (ship before pay, approve their own request)
- Race windows in check-then-act flows (balance checks, inventory, unique usernames)

## Supply chain

- Lockfile present and committed; new dependencies with install scripts; typosquatted names
- Dependencies pinned to a mutable git ref or `latest`
- Known CVEs: `osv-scanner -r .`, `npm audit --omit=dev`, `pip-audit`. Check reachability before calling one a finding

## CI/CD and infrastructure

- GitHub Actions: `pull_request_target` or `workflow_run` that checks out and runs PR code; `${{ github.event.* }}` interpolated into `run:`; third-party actions not pinned to a SHA; broad `permissions:`
- Secrets available to fork PRs; self-hosted runners that accept public PRs
- Containers running as root, `latest` tags, secrets baked into image layers
- Infrastructure: public buckets, `0.0.0.0/0` security groups, wildcard IAM, debug endpoints enabled in production

## LLM and agent tools

- Untrusted content (web pages, issues, emails, retrieved documents) placed into prompts that can trigger tools: prompt injection that leads to actions
- Tools with more authority than the task needs (write access, shell, network) and no confirmation step
- Model output used as SQL, shell, URL, HTML or file path without validation
- Agent workflows in CI that read attacker-authored text and then hold tokens with write scope

## Usually not a finding

Verify these before dismissing them. Do not assume.

- Values from operator-controlled config or constants
- Output that the framework auto-escapes (React `{x}`, Django `{{ x }}`, Vue `{{ x }}`)
- Parameterized queries and ORM filter calls
- Test fixtures and dead code, unless the audit is specifically about them
- Missing hardening with no concrete failure scenario. List it as a recommendation, not as a vulnerability
