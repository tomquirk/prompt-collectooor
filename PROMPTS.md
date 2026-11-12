# Prompt catalog

Generated from `prompts.json`; edit that file and rebuild.

## Testing and verification

<a id="browser-testing"></a>

### Browser testing across widths, touch, and slow networks

A web interface needs verification across screen sizes, touch input, and slow connections.

```text
Test this in the browser at different widths, with touch emulation, and on a throttled 3G connection. Fix anything that looks broken or feels off. Save a before and after screenshot for every fix and send me a summary afterwards.
```

Source: [@emilkowalski](https://x.com/emilkowalski/status/2120508498236596597) (unverified)

<a id="e2e-proof"></a>

### End-to-end proof

A completed feature needs end-to-end evidence that it works.

```text
test this e2e & give me irrefutable proof it works
```

Source: [@thorstenball](https://x.com/thorstenball/status/2102623376196194763) (unverified)

## Codebase audits and simplification

<a id="single-source-of-truth"></a>

### Single source of truth audit

The same fact or configuration may be maintained in multiple places.

```text
single source of truth audit
```

Source: [@kitlangton](https://x.com/kitlangton/status/2120341112959455559) (unverified)

<a id="full-project-audit"></a>

### Full project audit

A project needs a broad review of correctness, consistency, and unnecessary work.

```text
Read this entire project and find everything that's broken, inconsistent, inefficient, or no longer needed. Fix what you're sure about and list the rest for me to review.
```

Source: [@chenchengpro](https://x.com/chenchengpro/status/2120040764243894547) (unverified)

<a id="delete-and-simplify"></a>

### Delete, simplify, optimize, automate

Complexity or weak assumptions make a codebase harder to maintain.

```text
I want you to audit our codebase, is anything here unnecessary, overly complicated in our current setup, or based on weak assumptions? Challenge them.

- What can be deleted entirely?
- What can be simplified now that unnecessary pieces are gone?

Then make the changes. Prefer deleting over simplifying, simplifying over optimizing, and optimizing over automating.

This product is being used by thousands of customers, do not cut any corners.
```

Source: [@anthonyriera](https://x.com/anthonyriera/status/2119870644514893997) (unverified)

<a id="read-only-codebase-simplification-audit"></a>

### Read-only codebase simplification audit (summary)

You want evidence-backed simplification recommendations before authorizing code changes.

```text
Review the repository without changing it. Map its subsystems and boundaries, then examine each for worthwhile improvements to data structures, state representation, algorithms, control flow, and ownership. Use bounded, independent reviews where available. Keep a shared coverage record, including explicit decisions that no change is warranted.

Limit each subsystem to two strong recommendations, supported by file references, proposed changes, scope, risks, validation needs, and confidence. Independently check findings, remove duplicates and weak abstractions, and review coverage before ranking recommendations by impact and dependencies. Do not implement changes or run tests during the audit.

This is an editorial summary. Read the linked gist for the complete workflow.
```

Editorial summary; follow the source link for the full prompt.

Source: [@aarondfrancis](https://gist.github.com/aarondfrancis/8735edbe48532f97ee5ea818db4dbd47) (verified)

Related tweet: [https://x.com/aarondfrancis/status/2088285625946370352](https://x.com/aarondfrancis/status/2088285625946370352) (unverified)

## State machines and semantics

<a id="find-state-machines"></a>

### Find implicit state machines

An app has behavior that depends on changing state and events.

```text
find all of the implicit state machines in my app
```

Source: [@steveruizok](https://x.com/steveruizok/status/2116552016218710389) (unverified)

<a id="make-state-machines-explicit"></a>

### Make useful state machines explicit

Implicit state transitions may benefit from explicit modeling; the prompt references lavish-axi.

```text
audit and find implicit state machines in this <codebase/directory/module> that would drive concrete improvements if made explicit. explain before/after of each one and discuss with me in lavish-axi. fewer words, big visuals
```

Source: [@kunchenguid](https://x.com/kunchenguid/status/2119924895060795492) (unverified)

<a id="minimal-semantic-model"></a>

### Recover the minimal semantic model

Async behavior, duplicated state, or refactors need semantic analysis.

```text
Recover my program's minimal semantic model.

1. State: every value that changes what the user sees
2. Transitions: what commutes, what's idempotent, what's order-dependent
3. Dependencies: what must be true before each effect fires

Then find:
→ nondeterminism in awaits, retries and event order
→ invariants enforced by hope
→ one fact stored in two places, drifting
→ work that never reaches the screen

Last, split my refactors into "provably equivalent" and "trust me". For each "trust me", give the smallest input that breaks it.
```

Source: [@infinterenders](https://x.com/infinterenders/status/2119676620680339490) (unverified)

<a id="document-state-machines"></a>

### Document state machines and fix reachable bugs

Reachable invalid states need evidence, documentation, and regression-tested fixes.

```text
Find the app’s explicit and implicit state machines and document their states, invariants, and transition tables in one file. Identify invalid states or transitions the code can actually reach, with evidence, including through retries and concurrency. Prioritize confirmed bugs by impact, group related fixes into issues, then fix them with regression tests and keep the document updated.
```

Source: [@trevin](https://x.com/trevin/status/2118690987153186845) (unverified)

## Design and experience

<a id="simple-ux-dx-ax"></a>

### Simplicity across UX, DX, and AX

An interface or implementation feels cluttered or unnecessarily complex.

```text
I want this to be as perfect as Linear's website or Apple Notes: simple purpose, simple architecture, simple design, simple implementation. Cut taglines, helper text and secondary labels. If a screen needs them to make sense, fix the layout. Every decision should elevate the user experience (UX), developer experience (DX) and agent experience (AX) at once, without breaking anything.
```

Source: [@Voxyz_ai](https://x.com/Voxyz_ai/status/2117281830449942825) (unverified)

<a id="product-experience-coverage-audit"></a>

### Product experience coverage audit (summary)

You need a product-wide UX review with an actionable handoff for product, design, and engineering.

```text
Assess the current product without modifying its repository. Establish its users, goals, and constraints from workspace evidence. Track coverage of screens, states, and complete journeys, combining code inspection with safe runtime observation. Focus on desktop and tablet, including keyboard, touch, accessibility, and recovery behavior; phone optimization is generally excluded.

Coordinate bounded reviews, keeping shared browser sessions serialized. Support recommendations with concrete user consequences, screenshots where useful, implementation references, acceptance criteria, and validation needs. Check design-system ownership and only use competitor examples for demonstrated, contained gaps. Independently verify findings, record inaccessible or unverified areas, and prioritize small implementation slices with cross-functional handoffs.

This is an editorial summary. Read the linked gist for the complete workflow.
```

Editorial summary; follow the source link for the full prompt.

Source: [@tommymarshall](https://gist.github.com/tommymarshall/c8e25407aecd111573766c9f1456a412) (verified)

Related tweet: [https://x.com/tommyjmarshall/status/2091681150552989700](https://x.com/tommyjmarshall/status/2091681150552989700) (unverified)

## Performance

<a id="select-database-fields"></a>

### Select only the database fields you need

Database queries fetch whole rows while using only a few fields.

```text
find every place we load a whole row from the database just to read a couple of fields. instead, select only what we need
```

Source: not provided.

<a id="unnecessary-url-parsing"></a>

### Remove unnecessary URL parsing

Repeated or redundant URL parsing may add unnecessary work.

```text
remove all unnecessary `new URL()` parsing
```

Source: [@_dylanga](https://x.com/_dylanga/status/2117400205314421058) (unverified)

<a id="module-level-regexes"></a>

### Compute regexes at module level

Regexes are repeatedly constructed in functions or loops.

```text
compute all regexes at the module level instead of inside functions and loops
```

Source: [@_dylanga](https://x.com/_dylanga/status/2117400205314421058) (unverified)

<a id="jsonb-key-to-column"></a>

### Promote hot JSONB keys to columns

A hot path repeatedly reads a single key from a large JSONB value.

```text
find hot-path reads of a single key from a large jsonb column and promote that key to a real column
```

Source: [@_dylanga](https://x.com/_dylanga/status/2117400205314421058) (unverified)

<a id="parallel-async-calls"></a>

### Remove unnecessary sequential async calls

Independent async operations appear to run sequentially on hot paths.

```text
do a deep scan of all hot paths and fix any unnecessary sequential async function calls
```

Source: [@_dylanga](https://x.com/_dylanga/status/2117099613022732412) (unverified)

## Security and system cleanup

<a id="security-audit-dashboard"></a>

### Security audit, remediation, and dashboard

A project needs a security audit and evidence of remediation; the prompt references an external Cloudflare skill.

```text
Install Cloudflare’s security-audit skill globally and invoke its full audit workflow on this project.

github.com/cloudflare/sec — https://t.co/PoZZnDNiPy

Please implement this skill for my project repos or globally in my projects.

Independently verify findings, implement targeted fixes for confirmed vulnerabilities, and run relevant tests. Preserve unrelated changes.

Build an interactive security dashboard covering frontend, APIs, authentication, databases, infrastructure and dependencies. Show:
- Findings by severity and affected stack layer.
- Open, fixed and verified remediation status.
- Security posture before and after fixes.
- Source evidence, code changes and test results.
- Audit coverage, unverified areas and remaining priorities.

Base posture assessments on evidence and clearly label coverage gaps.
```

Source: [@thejoegardiner](https://x.com/thejoegardiner/status/2118119394517950725) (unverified)

<a id="macos-cleanup"></a>

### Remove unused macOS software and permissions

The user explicitly wants to review and remove unused macOS software and permissions.

```text
remove all the apps, tcc/permission grants, login items, daemons, kexts, browser exts, homebrew packages, etc., that I don't need and use.
```

Source: [@sqs](https://x.com/sqs/status/2120113139996086409) (unverified)

<a id="live-web-app-security-audit"></a>

### Read-only security audit of a live web app

A web app or SaaS is live (or about to launch) and you want an evidence-based audit of auth, APIs, database access, config, and business logic before fixing anything.

```text
My web application is live. Act as a Senior Application Security Engineer and perform a thorough security audit.

Don't give me generic security advice. Inspect the actual codebase, trace important code paths, and identify vulnerabilities that could put user accounts, data, or business operations at risk.

1. Authentication & Authorization
- Review login, signup, logout, and session handling.
- Verify that permissions are checked on the server.
- Check whether users can access other users' private data.
- Look for IDOR and Broken Object Level Authorization (BOLA).
- Test whether normal users can access admin-only endpoints.
- Review password reset and email verification flows.
- Check session expiration and token handling.

2. API & Backend Security
- Inspect every important API endpoint.
- Check for SQL injection and unsafe database queries.
- Look for XSS, CSRF, and SSRF vulnerabilities.
- Check for mass assignment and privilege escalation.
- Validate all user-controlled input on the server.
- Review file uploads, downloads, and access permissions.
- Check whether sensitive endpoints have proper rate limits.
- Verify webhook signatures and prevent replay or duplicate processing where applicable.

3. Database & Secrets
- Review database permissions and Row Level Security policies.
- Check whether RLS is enabled and correctly enforced where required.
- Look for exposed API keys, credentials, and private environment variables.
- Check whether frontend code exposes sensitive backend information.
- Verify that users can only read and modify records they're authorised to access.
- Review database functions and privileged operations.

4. Configuration & Infrastructure
- Review CORS configuration.
- Check security headers and cookie settings.
- Look for insecure redirects and exposed internal endpoints.
- Review dependency vulnerabilities.
- Check production and development environment separation.
- Inspect error handling for leaked stack traces or sensitive information.
- Make sure application logs don't contain passwords, tokens, or private user data.

5. Business Logic
- Check whether users can bypass payment or subscription restrictions.
- Look for ways to manipulate prices, quantities, or account privileges.
- Test whether users can repeat actions that should only happen once.
- Check whether ownership is verified before modifying or deleting records.
- Review invitation, referral, and account management flows where applicable.

IMPORTANT INSTRUCTIONS:
- Start with a read-only audit.
- Only test systems I own or am explicitly authorised to assess.
- Use local or staging environments and test accounts wherever possible.
- Never expose actual secrets in your report.
- Don't delete data or change production configuration.
- Don't disable existing security protections.
- Don't claim a vulnerability exists without evidence.
- Don't automatically change code during the audit.

For every confirmed issue, provide:
- Severity: Critical, High, Medium, or Low.
- Exact file and code location.
- What the vulnerability is.
- How it could be exploited.
- What data or functionality is at risk.
- The recommended fix.
- A test to verify that the fix works.

Finally, rank the issues by priority and give me a practical remediation plan.

After I approve the fixes, implement them in a separate development branch, add regression tests, and show me the changes. Never deploy without explicit approval.
```

Source: [@Sujay__Raj](https://x.com/Sujay__Raj/status/2120831910675145189) (verified)

## Agent workflows and retrospectives

<a id="weekly-session-review"></a>

### Review last week's sessions and suggest improvements

Recent coding sessions are available and the user wants to identify ways to improve their workflow.

```text
look at last weeks sessions and suggest improvements
```

Source: [@nateberkopec](https://x.com/nateberkopec/status/2114842635743674790) (unverified)
