# Manual foundation pilot

The first supervised foundation tasks exposed execution-readiness checks that are not
captured by task schema validation alone.

## Generated paths

Framework commands may create tracked files that are absent from an initial scaffold.
For example, a Next.js build can generate `next-env.d.ts`. Before approving a task,
identify files produced by its setup, generation, build, and test commands and include
each tracked output in the task boundary. Do not broaden paths after execution begins
when a focused generated-file amendment is sufficient.

## Verification provenance

A verification command is runnable only when it already exists or is introduced by the
task or one of its completed dependencies. Acyclic task IDs are insufficient: record
which task owns every package script, test harness, generated tool, service, and runtime
prerequisite. Sequence consumers after that owner.

Avoid hidden infrastructure assumptions. Configuration-only database work must not
claim live integration evidence without an approved disposable database mechanism.

## Environment prerequisites

Separate prerequisites into:

- repository dependencies and lockfile changes
- downloaded tool artifacts such as browser binaries
- operating-system libraries
- external services and credentials
- interactive privileges such as `sudo`

Approval for one category does not imply approval for another. Non-interactive agents
cannot supply an interactive `sudo` password; perform that bounded action manually or
pre-provision the isolated environment.

## Partial-plan language

Task coverage in a partial plan means the task contributes approved foundation work.
It does not prove complete satisfaction of the underlying product requirement or
acceptance criterion. Report validator success as complete partial-plan accounting and
preserve full product verification as later-wave work.

## Parallel implementation

Land shared approval and governance changes before creating parallel implementation
branches. Then create one isolated branch or worktree per task from the same approved
base. Concurrent tasks must not edit shared implementation paths or shared governance
files.

Do not push approval changes directly to a protected integration branch. Use a small
approval-only pull request when branch policy requires pull requests for `dev`.

## Review findings

Treat blocking findings as merge gates. Record non-blocking findings without
automatically expanding a proof-of-concept task. Verify automated reviewer claims
against current primary documentation and observed dependency behavior before changing
code; reviewer confidence is not evidence by itself.
