# Report template

Use this format after the mark step. Use the summary from `sweep.py mark` as evidence.
The report has two tables: the done threads and the threads that need action.
Use the same columns, order, and text as the confirmed proposal. Remove the row numbers.

## Template

    I marked {marked count} of {total} threads as done. {action count} threads need your action.

    ## Marked as done

    | Thread | Action | Reason |
    | --- | --- | --- |
    | [{owner/repo#N}]({url}) {title} | Done | {reason} ({rule}) |

    ## Needs your action

    | Thread | Action | Group | Reason |
    | --- | --- | --- | --- |
    | [{owner/repo#N}]({url}) {title} | {action} | {Yours or Others} | {reason} {one direct command} ({rule}) |

## Rules for the content

- Put a thread in "Marked as done" only if the script lists it under `marked`.
- Put each changed or failed thread in "Needs your action" with the action "Check". Put these rows last.
- For a changed thread, write "The thread changed after the collect step. Run the sweep again."
- For a failed thread, give the error from the script. Then write "Run the sweep again later."
- For a row that the user moved with `keep`, write "You kept this thread." Then give the command.
- If the user replied `no`, write "I marked no threads." Then rename "Marked as done" to "Proposed done (not marked)".
- Write "None." for a table without rows.
