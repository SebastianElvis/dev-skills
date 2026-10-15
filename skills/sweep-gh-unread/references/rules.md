# Classification rules

The script `scripts/sweep.py` applies these rules to each notification thread.
In each table, the first row that matches sets the result.
A `judge` result means that the agent decides if a reply needs an answer.

## Terms

- **You**: the user that `gh api user` returns.
- **Your team**: a team that `gh api user/teams` returns.
- **Human**: an author that is not a GitHub bot.
- **Your note**: a comment, a review comment, or a review by you.
- **Open reply**: a human note by another person after your last note. The note must be in one of these places:
  - an unresolved review thread with your comment;
  - any unresolved review thread on your PR;
  - a top-level comment or a review body on your PR;
  - a top-level comment or a review body that mentions you on another PR or an issue.
- **Author response**: a note by the PR author after your last review. A resolved thread from your last review is also an author response.
- **Your review**: a submitted review by you in any state.

## All threads

| Rule | Condition | Result |
| --- | --- | --- |
| N1 | The type is `CheckSuite`, `WorkflowRun`, `Release`, or a Dependabot or security alert. | Done |
| E1 | The script cannot read the PR or the issue. | Action: check |

## Pull requests

| Rule | Condition | Result |
| --- | --- | --- |
| P1 | The PR is merged or closed. | Done |
| P2 | A bot is the author of the PR, such as Dependabot. | Done |
| P3 | The PR is in the merge queue. | Done |

## Your PRs

| Rule | Condition | Result |
| --- | --- | --- |
| Y1 | The PR has an open reply. | Judge: reply, or the next rule |
| Y2 | A reviewer requested changes, CI failed, or the PR has a merge conflict. | Action: fix |
| Y3 | The PR is approved, mergeable, and not a draft. | Action: merge |
| Y4 | No other rule applies. The PR waits for reviewers. | Done |

## PRs of other authors

| Rule | Condition | Result |
| --- | --- | --- |
| O1 | The PR is a draft. | Done |
| O2 | The PR has an open reply. | Judge: reply, or the next rule |
| O3 | You or your team got a review request at any time, and you have no review. A review by a teammate does not change this. | Action: review |
| O4 | You have a review, and a review request to you or your team is open again. | Action: re-review |
| O5 | Your last approval or change request is an approval, and no new request exists. | Done |
| O6 | You have a review, and the author responded after your last review. | Action: re-review |
| O7 | You have a review, and the author did not respond after it. A new commit alone is not a response. | Done |
| O8 | You got no review request, and you have no review. | Done |

## Issues and other types

| Rule | Condition | Result |
| --- | --- | --- |
| N2 | The issue is closed. | Done |
| N3 | The notification assigns the open issue to you, or the issue has an open reply. | Action: check, or judge |
| N4 | The issue is open, and no other rule applies. | Done |
| N5 | The type has no rule, such as `Discussion` or `RepositoryAdvisory`. | Action: check |

## Change a rule

Change `classify_pr` or `classify_issue` in `scripts/sweep.py` and this file together.
Add a thread for the new rule to `evals/skills/sweep-gh-unread/fixture/make_fixture.py`.
Then run `python3 -m unittest discover -s evals/skills/sweep-gh-unread`.
