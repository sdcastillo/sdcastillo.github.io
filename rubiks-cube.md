---
layout: default
title: A Rubik’s Cube may be solved systematically layered by layer
description: Sam Castillo’s beginner 3×3 Rubik’s Cube tutorial, with algorithm slides and flashcards.
permalink: /rubiks-cube/
samwiki: true
---

<link rel="stylesheet" href="/assets/rubiks-cube/cube.css">


<div class="cube-lab" id="cube-lab" tabindex="0">
  <h1>A Rubik’s Cube may be solved systematically layered by layer</h1>
  <p class="lede">Sam Castillo’s beginner method for the 3×3. Seven steps, one algorithm at a time. Watch the tutorial, page through the slides, then drill the moves with the flashcards.</p>
  <p class="meta">A layered solve, not speedcubing — hold the cube as the slides show, and only turn the faces the algorithm names.</p>

  <h2 id="tutorial">Tutorial</h2>
  
<div class="cube-frame cube-player" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
  <iframe style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
          src="https://rumble.com/embed/v7g3dzi/?pub=4nnnxw"
          title="A Rubik’s Cube may be solved systematically layered by layer"
          frameborder="0"
          allowfullscreen></iframe>
</div>
<p class="meta"><a href="https://rumble.com/v7i9qx0-a-rubiks-cube-may-be-solved-systematically-layered-by-layer.html?mref=4nnnxw">Watch on Rumble</a></p>


  <h2 id="slides">Algorithm slides</h2>
  <div class="cube-slides">
    <div class="cube-frame">
      <img class="slide cube-slide-img" id="cube-slide-img" src="/assets/rubiks-cube/slides/slide_01.jpg" alt="How to Solve a Rubik’s Cube — seven steps, seven algorithms">
    </div>
    <div class="cube-slide-nav">
      <button type="button" id="cube-prev-slide">Previous</button>
      <p class="cube-caption" id="cube-caption">1 / 9 — How to Solve a Rubik’s Cube — seven steps, seven algorithms</p>
      <button type="button" id="cube-next-slide">Next</button>
    </div>
    <div class="cube-dots" id="cube-dots" role="tablist" aria-label="Slides"></div>
    <p class="meta">Download the slides: <a href="/assets/rubiks-cube/downloads/Rubik_s_Cube_Cheat_Codes.pdf">PDF</a> · <a href="/assets/rubiks-cube/downloads/Rubik_s_Cube_Cheat_Codes.pptx">PowerPoint</a></p>
  </div>

  <h2 id="method">The seven steps</h2>
  <ol class="cube-steps">
    <li><span class='step-label'>Step 1 · White Cross</span> Build a white plus sign on top, with side colors matching the centers. Most of this is visual. To flip an edge that is in place but upside down: <span class='algo'>F U' R U</span>.</li>
<li><span class='step-label'>Step 2 · White Corners</span> Finish the white face and the first-layer ring. Park the corner directly below its target, then repeat <span class='algo'>R' D' R</span>.</li>
<li><span class='step-label'>Step 3 · Middle Layer</span> Flip the cube so yellow is on top. Match a non-yellow top edge to its side center, then insert. Right: <span class='algo'>U R U' R' U' F' U F</span>. Left: <span class='algo'>U' L' U L U F U' F'</span>.</li>
<li><span class='step-label'>Step 4 · Yellow Cross</span> Make a yellow plus sign. Start from a dot, a backward L (held top-left), or a horizontal line, and repeat <span class='algo'>F R U R' U' F'</span>.</li>
<li><span class='step-label'>Step 5 · Yellow Edges (Sune)</span> Hold two already-matching edges at the back and right, then do <span class='algo'>R U R' U R U2 R'</span>.</li>
<li><span class='step-label'>Step 6 · Position Corners (Niklas)</span> Get each yellow corner into the right seat, even if it is twisted. Hold a correct corner in front-right and repeat <span class='algo'>U R U' L' U R' U' L</span>.</li>
<li><span class='step-label'>Step 7 · Orient Corners</span> Put an unsolved corner in front-right and repeat <span class='algo'>R' D' R D</span> until yellow faces up. Then turn <em>only</em> the top layer (<span class='algo'>U</span>) to bring the next corner over — rotating the whole cube will scramble the layers you already solved.</li>
  </ol>

  <h2 id="flashcards">Flashcards</h2>
  <p>Thirty-five cards from the tutorial. Click a card to flip it, or use the arrow keys and the space bar.</p>
  <div class="cube-filters" role="group" aria-label="Filter by step">
    <button type="button" data-filter="all" aria-pressed="true">All</button>
<button type="button" data-filter="1" aria-pressed="false">Step 1</button>
<button type="button" data-filter="2" aria-pressed="false">Step 2</button>
<button type="button" data-filter="3" aria-pressed="false">Step 3</button>
<button type="button" data-filter="4" aria-pressed="false">Step 4</button>
<button type="button" data-filter="5" aria-pressed="false">Step 5</button>
<button type="button" data-filter="6" aria-pressed="false">Step 6</button>
<button type="button" data-filter="7" aria-pressed="false">Step 7</button>
  </div>
  <div class="cube-card-wrap">
    <div class="cube-card-stage">
      <button type="button" class="cube-flip" id="cube-flip" aria-pressed="false" aria-label="Flip flashcard">
        <span class="cube-flip-inner">
          <span class="cube-face cube-front">
            <span class="cube-kicker cube-kicker-q">Question</span>
            <span class="cube-q" id="cube-q"></span>
          </span>
          <span class="cube-face cube-back">
            <span class="cube-kicker cube-kicker-a">Answer</span>
            <span class="cube-a" id="cube-a"></span>
          </span>
        </span>
      </button>
    </div>
    <div class="cube-card-nav">
      <button type="button" id="cube-prev-card">Previous</button>
      <button type="button" id="cube-next-card">Next</button>
      <button type="button" id="cube-shuffle">Shuffle</button>
      <span class="cube-progress" id="cube-progress"></span>
    </div>
    <p class="cube-hint">Tip: filter to one step and shuffle it until the algorithm is automatic.</p>
  </div>

  <p class="cube-tags">#rubikscube #speedcubing #rubikscubesolve #satisfying #puzzle #cubing #fyp #viral #brainteaser #math #rubikscubetutorial #howtosolvearubikscube #cubetutorial #3x3 #3x3rubikscube #beginnercubing #learntocube #layerbylayer #layeredmethod #beginnermethod #cubealgorithms #whitecross #yellowcross #sune #twistypuzzle #oddlysatisfying #puzzlesolving #tutorial #educational #STEM #rubixcube #rubixcubetutorial</p>
</div>
<script>
window.CUBE_PAGE = {
  slides: [{"src": "/assets/rubiks-cube/slides/slide_01.jpg", "caption": "How to Solve a Rubik’s Cube — seven steps, seven algorithms"}, {"src": "/assets/rubiks-cube/slides/slide_02.jpg", "caption": "Step 1: The White Cross — F U' R U"}, {"src": "/assets/rubiks-cube/slides/slide_03.jpg", "caption": "Step 2: The White Corners — R' D' R"}, {"src": "/assets/rubiks-cube/slides/slide_04.jpg", "caption": "Step 3: The Middle Layer — flip the cube, then right or left insert"}, {"src": "/assets/rubiks-cube/slides/slide_05.jpg", "caption": "Step 4: The Yellow Cross — F R U R' U' F'"}, {"src": "/assets/rubiks-cube/slides/slide_06.jpg", "caption": "Step 5: Match the Edges — the Sune algorithm"}, {"src": "/assets/rubiks-cube/slides/slide_07.jpg", "caption": "Step 6: Move the Corners — the Niklas algorithm"}, {"src": "/assets/rubiks-cube/slides/slide_08.jpg", "caption": "Step 7: Twist to Win — R' D' R D, and only turn the top layer"}, {"src": "/assets/rubiks-cube/slides/slide_09.jpg", "caption": "You did it — the roof, the walls, and the foundation"}],
  cards: [{"q": "How many total steps are in this beginner Rubik's Cube solving guide?", "a": "7 steps", "step": 0}, {"q": "What is the goal of Step 1 (White Cross)?", "a": "Form a white plus sign on the top face with edge colors matching the side center colors.", "step": 1}, {"q": "In Step 1 (White Cross), what algorithm flips a white edge piece that is in place but upside down?", "a": "F U' R U", "step": 1}, {"q": "What is the main technique used for most of Step 1 (White Cross)?", "a": "Intuitive movement (solving by visual awareness without fixed algorithms for most pieces).", "step": 1}, {"q": "What is the main goal of Step 2 (White Corners)?", "a": "Complete the white face and solve the entire bottom layer ring.", "step": 2}, {"q": "What algorithm is repeated to insert a corner piece during Step 2 (White Corners)?", "a": "R' D' R", "step": 2}, {"q": "Where must a target white corner piece be placed before executing the R' D' R algorithm in Step 2?", "a": "Directly below its target spot on the bottom right.", "step": 2}, {"q": "What cube reorientation must be done before starting Step 3 (Middle Layer)?", "a": "Flip the cube over so that the yellow center face is on top.", "step": 3}, {"q": "What is the goal of Step 3 (Middle Layer)?", "a": "Solve the four middle-layer edge pieces.", "step": 3}, {"q": "Before solving a middle-layer edge piece in Step 3, how do you line it up on top?", "a": "Match a non-yellow top edge piece with its matching side center color.", "step": 3}, {"q": "What is the Step 3 algorithm for dropping a top edge piece into the Right middle layer slot?", "a": "U R U' R' U' F' U F", "step": 3}, {"q": "What is the Step 3 algorithm for dropping a top edge piece into the Left middle layer slot?", "a": "U' L' U L U F U' F'", "step": 3}, {"q": "What is the main goal of Step 4 (Yellow Cross)?", "a": "Create a yellow plus sign on the top face.", "step": 4}, {"q": "What algorithm is used to build the yellow plus sign in Step 4?", "a": "F R U R' U' F'", "step": 4}, {"q": "What initial yellow top-face patterns can you start with in Step 4?", "a": "A single dot, a backward “L”, or a horizontal line.", "step": 4}, {"q": "How must a backward “L” shape be positioned on top before running the Step 4 algorithm?", "a": "Held in the top-left corner of the top face.", "step": 4}, {"q": "How must a yellow line be held on the top face before performing the Step 4 algorithm?", "a": "Horizontally across the top face.", "step": 4}, {"q": "What is the goal of Step 5 (Yellow Edges)?", "a": "Align the yellow cross edges with their corresponding side center colors.", "step": 5}, {"q": "What sequence of moves makes up the Step 5 (Yellow Edges) algorithm?", "a": "R U R' U R U2 R'", "step": 5}, {"q": "What common name is given to the Step 5 algorithm (R U R' U R U2 R')?", "a": "The Sune algorithm.", "step": 5}, {"q": "How should the cube be held when executing the Sune algorithm in Step 5?", "a": "Hold two matching side edges at the back and right faces.", "step": 5}, {"q": "What is the goal of Step 6 (Position Corners)?", "a": "Move all four yellow corner pieces into their correct locations between side centers (even if twisted).", "step": 6}, {"q": "What is the move sequence for the Step 6 algorithm?", "a": "U R U' L' U R' U' L", "step": 6}, {"q": "What common name is given to the algorithm U R U' L' U R' U' L in Step 6?", "a": "The Niklas algorithm.", "step": 6}, {"q": "Where should a correctly positioned corner piece be held when performing Niklas in Step 6?", "a": "In the front-right top corner position.", "step": 6}, {"q": "Does a yellow corner need to have yellow facing up to be considered ‘positioned’ in Step 6?", "a": "No, it only needs to be in the correct spot between matching side colors, even if its colors are twisted.", "step": 6}, {"q": "What is the goal of Step 7 (Orient Corners)?", "a": "Twist the yellow corner pieces so that yellow faces up, completing the solve.", "step": 7}, {"q": "What algorithm is repeated to orient each yellow corner in Step 7?", "a": "R' D' R D", "step": 7}, {"q": "Where do you place an unsolved corner before running R' D' R D in Step 7?", "a": "In the front-right top position.", "step": 7}, {"q": "In Step 7, after solving one corner, how do you bring the next unsolved corner into position?", "a": "Turn ONLY the top layer (U) to move the next corner into the front-right position.", "step": 7}, {"q": "Why is it critical to turn ONLY the top layer (U) when moving to the next corner in Step 7?", "a": "Rotating the whole cube will scramble the bottom layers that were already solved.", "step": 7}, {"q": "The algorithm used in Step 5 to align yellow edges (R U R' U R U2 R') is known as the _____ algorithm.", "a": "Sune", "step": 5}, {"q": "The algorithm used in Step 6 to position corners (U R U' L' U R' U' L) is known as the _____ algorithm.", "a": "Niklas", "step": 6}, {"q": "Which step requires turning yellow to the top face before continuing?", "a": "Step 3 (Middle Layer)", "step": 3}, {"q": "In Step 7 (Orient Corners), how do you know when to stop repeating R' D' R D on a corner?", "a": "When the yellow color of that corner is facing up.", "step": 7}]
};
</script>


<script src="/assets/rubiks-cube/cube.js"></script>
