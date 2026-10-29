# Wordle Solver

A Python helper for Wordle. It ranks every allowed five-letter word by how common its letters are, suggests the highest scoring word as an opening guess, and then narrows the list down using the green, yellow and grey clues from each turn.

## How it works

Each word gets two scores. The positional score rewards letters that often appear in that exact position across the word list, which is what tends to produce greens. The occurrence score rewards letters that are common anywhere in a word, counting each distinct letter once, which is what tends to produce yellows. Both are scaled to between 0 and 1 and added together with a weight on each, and the list is sorted by the result.

After a guess, any word that does not fit the clues is removed. Matched letters are blanked out as the filter goes, so a word with a double letter is handled properly.

The `parameterSelection` folder is for tuning the two weights. It plays simulated games against random answers and uses the average number of guesses as the thing to minimise. There is a particle swarm search over both weights, a Bayesian optimisation over the positional weight alone with the other fixed at 1, and a few scripts for plotting the results as heatmaps or an animation of the swarm.

## Running it

Run the solver from the repository folder, since it loads `possibleWords.txt` by relative path:

```
python solve.py
```

It prints an opening guess, then asks for the clues. Green and yellow are entered as five characters with `.` for blanks, for example `..a.e`. Grey letters are entered as a plain list, such as `rts`.

The parameter selection scripts are run from inside `parameterSelection`. They read the word list with a Windows style path, and `paramSelectVisual.py` uses a Windows notification, so they are written for Windows. `paramSelectVisualAnim.py` also expects a local copy of ffmpeg at a hard-coded path.

## Files

- `solve.py` scores the words and runs the interactive solver.
- `possibleWords.txt` is the list of allowed guesses and `possibleAnswers.txt` the list of possible answers.
- `failures.py` was used to play through the answer list and print the words the solver could not get in six guesses. `failedWords.txt` holds a saved list of these. It imports a `bestGuess` function that is no longer in `solve.py`, so it will not run as things stand.
- `filterTest.py` was used to check the clue filter and has the same import problem.
- `parameterSelection/` holds the weight tuning scripts described above.

## Dependencies

The solver itself only needs the standard library. The parameter selection scripts use numpy, matplotlib, scipy and scikit-learn, plus win11toast for `paramSelectVisual.py`. They are listed in `requirements.txt`:

```
pip install -r requirements.txt
```
