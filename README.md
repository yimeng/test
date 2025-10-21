# Git Branch Practice Repository

This repository is a minimal sandbox for exploring Git branching and merge workflows. It contains only a handful of text documents that capture branch histories, merge experiments, and conflict examples.

## Repository Layout
- `README.md`: Overview of the repository and learning pointers for contributors.
- `branch1` – `branch4`: Notes that document what happened on each example branch. The file `branch4` intentionally retains merge-conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) so you can study and resolve conflicts by hand.
- `master`: Records the steps performed on the main branch during the exercises.
- `Untitled Diagram.drawio`: A Draw.io diagram reserved for illustrating branch relationships or workflows.

## Getting Started
1. Clone the repository and inspect the history with `git log --graph --oneline --all` to visualize how the sample branches diverge and merge.
2. Read through the `branch*` and `master` files to understand the scenarios being demonstrated and note where conflicts arose.
3. Recreate the `branch4` merge locally, practice resolving the conflict markers, and compare your results with the recorded notes.
4. Expand this README or add new exercises as you refine your understanding of Git operations.

## Next Steps for Learners
- Supplement the notes with a more detailed narrative or screenshots of Git commands to build a comprehensive tutorial.
- Add small sample projects or unit tests to make the repository resemble a real-world workflow and practice merging code changes instead of plain text.
- Document common Git tips, such as using `git status`, `git diff`, or interactive rebase, directly in the README or dedicated guides.
