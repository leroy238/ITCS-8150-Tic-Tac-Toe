# Current tasks

<ol>
  <li>Discuss the project, goals, and task designation.</li>
  <li>Program the game.
    <ul>
      <li>Game stored in 3D Array</li>
      <li>Turns are Boolean and single-threaded</li>
      <li>Numbers in the array to store where the Player and AI tokens are.</li>
      <li>GUI reads the data as we store it.</li>
      <li>Max depth is based on the difficulty.</li>
      <li>Player first, then AI.</li>
    </ul>
  </li>
  <li>Program the GUI.
    <ul>
      <li>How do we handle user interactions?</li>
      <li>How often do we update the screen?</li>
      <li>Is the GUI asynchronous with the underlying game?</li>
      <li>If so, do we need to ensure that the screen updates with the user turn before the AI does theirs?</li>
      <li>Are we including menu flairs (hovering over items changes size/shape/color) or will it be static?</li>
      <li>What is the aesthetic theme? Should we worry about high contrast for colorblind users?</li>
    </ul>
  </li>
  <li>Program the AI.
    <ul>
      <li>Minimax algorithm.</li>
      <li>Alpha-Beta algorithm.</li>
      <li>Difficulty levels.</li>
      <li>Heuristic function.</li>
      <li>Goal checking implementation?</li>
    </ul>
  </li>
</ol>

# Grading Rubric + Where are we?

## Implementation (15 points)

Program utilizes alpha beta procedure and runs properly for all 3 difficulty levels. (15)

Program does not utilize alpha-beta procedure but runs properly for all 3 difficulty levels. (10)

Program implements 3 dimiensional tic-tac-toe game but has some errors and the same does not run properly. (5)

&#x2611; *Nothing (0)*

## Documentation (5 points)

Explaining all steps of the program. (5)

Explaining most steps of the program. (3)

Explaining some steps of the program. (2)

&#x2611; *No documentation (0)*

## Interface (10 points)

Interactive interface works properly and is nicely done. (10)

Interactive interface works properly. (8)

Works partially. Not for all three levels. It has some errors. (4)

&#x2611; *This function is not implemented. (0)*
