# CLAUDE.md

This file provides guidance for AI assistants working in this repository.

## Repository Overview

This is a personal Git learning and practice repository. It contains small text
files used to experiment with Git commands, branching, merging, committing, and
other version-control workflows. There is no application to build or test suite
to run.

**Author:** SAK JAE LIM (aicpakevin@gmail.com)

---

## Repository Structure

```
first-repo/
├── CLAUDE.md        # This file
├── a.txt            # Practice text file (contains "A" and "B")
├── b.txt            # Practice text file
├── file1.py.txt     # Misnamed text file (not a Python source file)
├── file2.py         # Small text file with test content
└── new1.txt         # Text file with content in Korean ("뉴진스 화이팅")
```

No build system, package manager, linter, or test runner is configured.

---

## Git Conventions

### Commit Messages
- Commit messages are written in **Korean**.
- Messages are short and descriptive (e.g. `첫번째 커밋`, `두번째 커밋`, `삭제`).
- Follow the same style when making commits in this repository.

### Branches
- `master` — primary local branch.
- `claude/*` — branches created by AI assistants (e.g. `claude/add-claude-documentation-RmqeQ`).
- Feature branches follow the pattern `claude/<description>-<id>`.

### Typical Git Workflow
1. Create or switch to a working branch.
2. Make file changes.
3. Stage with `git add <file>`.
4. Commit with a short Korean or English message.
5. Push with `git push -u origin <branch-name>`.

---

## Working in This Repository

### Making Changes
- This repo contains only plain text files. Edit them directly.
- There is no build step, compilation, or dependency installation required.
- Changes are verified by reading the file content — no automated tests exist.

### What AI Assistants Should Do
- Keep changes **minimal and focused** on what was requested.
- Use the branch `claude/<description>-<sessionId>` for all AI-driven work.
- Commit with clear messages before pushing.
- Do **not** add unnecessary files, directories, or boilerplate.

### What AI Assistants Should Avoid
- Do not introduce a build system, test framework, or linting config unless explicitly requested.
- Do not rename or restructure existing files without explicit instruction.
- Do not push to `master` or `main` without explicit permission.

---

## Development Workflow (AI Orchestration)

### Planning
- For any task with 3+ steps or architectural decisions, plan before acting.
- Write a checklist in `tasks/todo.md` (create the file if it does not exist).
- Verify the plan before starting implementation.

### Execution
- Mark checklist items complete as you finish them.
- If something is blocked or goes wrong, stop and re-plan — do not push through.
- Never mark a task complete without confirming the change is correct.

### Lessons
- After any user correction, record the pattern in `tasks/lessons.md`.
- Review `tasks/lessons.md` at the start of each new session for relevant context.

---

## Key Facts for AI Assistants

| Item | Value |
|---|---|
| Primary branch | `master` |
| AI work branch prefix | `claude/` |
| Language of commits | Korean (preferred) |
| Test command | None |
| Build command | None |
| Package manager | None |
