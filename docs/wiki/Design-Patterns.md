## 🎯 Objective
This document aims to standardize development practices across all project repositories, promoting consistency, readability, and efficient collaboration among team members. The guidelines apply to all stakeholders, including Frontend, Backend, and ETL teams.

<br>

## 🧩 Summary
- 🚀 <a href="#branch-pattern">Branch Pattern</a>
- 📦 <a href="#commit-pattern">Commit Pattern</a>
- 🚧 <a href="#pull-request-pattern">Pull Request Pattern</a>
- 📌 <a href="#guidelines">Guidelines</a>
- 👀 <a href="#code-review">Code Review</a>
- 🔖 <a href="#version-tag-pattern">Version Tag Pattern</a>
- ✅ <a href="#definition-of-done">Definition of Done (DoD)</a>
- 🟢 <a href="#definition-of-ready">Definition of Ready (DoR)</a>

<br>

<span id="branch-pattern">

## 🚀 Branch Pattern

### 🌿 Main Branches
	01-creation-of-project-repositories
<br>

<span id="commit-pattern">

## 📦 Commit Pattern

### 🔤 Format:
	feat: Creation of project repositories

<br>

<span id="pull-request-pattern">

## 🚧 Pull Request Pattern

### 🔤 Format:
~~~shell
{GitHub issue code} - [Type] Short description of the change
~~~
### Allowed types:
- `[Feature]` - New functionality.
- `[Fix]` - Bug fix.
- `[Docs]` - Documentation.
- `[Refactor]` - Code refactoring.
- `[Chore]` - Internal maintenance.
### ✅ Example:
~~~shell
01 - [Feature] Creating project repositories
~~~

<br>

<span id="guidelines">

## 📌 Guidelines:
- Every new feature or fix must go through PR.
- When opening the PR:
  - Tag at least 1 reviewer from the team.
  - Add the link to the Jira/Taiga issue.
  - Make a clear description of what was changed.
  - Make sure the branch is up to date with the sprint branch.

<br>

<span id="code-review">

## 👀 Code Review
- Every PR must be reviewed by at least **one team member**.
- The reviewer must check:
  - Clarity and readability of the code.
  - Test coverage (if applicable).
  - Impact on other parts of the system.
  - Good practices and standards defined here.
> No PR should be merged without approval and without `success` in the CI workflow.
<br>

<span id="version-tag-pattern">

## 🔖 Version Tag Pattern

### 🔤 Format:
	sprint - {number}

### ✅ Example:

        sprint - 1

> Use tags to mark relevant deliveries or sprint closures.
<br>

<span id="definition-of-done">

## ✅ Definition of Done (DoD)

Minimum criteria to consider a task as **complete**:
	Minimum criteria to consider a task as **complete**:
* Code implemented
* Tests executed
* Documentation updated
* API documentation completed
* Delivery presentation videos

<br>

<span id="definition-of-ready">

## 🟢 Definition of Ready (DoR)

Minimum criteria to consider a task **ready for development**:
* User stories with acceptance criteria
* Defined subtasks
* Defined design
* Database modeling
* System architecture definition
* Sprint planning