#!/usr/bin/env bash
# Create a repository with an obsolete diagram.
set -euo pipefail
dir="$(mktemp -d -t visualize-arch-eval-XXXXXX)"
cd "$dir"
git init -q -b main
git config user.email eval@example.com
git config user.name Eval
git config commit.gpgsign false
git config core.hooksPath /dev/null
mkdir -p src docs/assets
cat > src/worker.py <<'PY'
def run_worker(queue, carrier, database):
    job = queue.next_job()
    try:
        result = carrier.send(job)
    except TimeoutError:
        database.mark_failed(job)
        return "failed"
    database.save_result(job, result)
    return "sent"


PROVIDER = "ParcelCarrier"
PY
cat > docs/assets/worker.tex <<'TEX'
\documentclass[tikz,border=4pt]{standalone}
\usetikzlibrary{arrows.meta,positioning}
\begin{document}
\begin{tikzpicture}[every node/.style={draw,font=\sffamily\small}]
\node (worker) {Worker};
\node[right=of worker] (carrier) {LegacyCarrier};
\draw[-{Latex}] (worker) -- (carrier);
\end{tikzpicture}
\end{document}
TEX
cat > docs/assets/Makefile <<'MAKE'
SOURCE = worker.tex
all:
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(SOURCE)
	pdftocairo -svg worker.pdf worker.svg
MAKE
git add .
git commit -q -m "Add the current worker and obsolete diagram"
echo "$dir"
