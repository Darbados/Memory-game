# Memory-game

Here is a short description of my solution of the Memory-game.
It was indeed nice challenge and chance to take different approach from what I'm ussually doing, i.e. making a desktop version with GUI.
So I've started with trying to break the whole problem into small problems in order to be able to represent each small piece as a code snippet.
So what are the pieces of the whole picture in terms of having this in GUI?
1. We need a screen, which should have its size parameters ( Width, Height ).
2. We need to declare some shapes which will stand as couples of cards that the players will look for. Here I'm using extreme simple forms that pygame can draw.
3. We need something specific for our couples of shape which is the same per couple - color. Pygame is the provider of the colors as well.
4. We need to be sure that all of our combinations are not less than the half of our boxes that well display - so there is an 'assert' statement that works for this.
5. In order to get the position of our cards on the screen, I make some calculations for x & y margin, which are based on the screen width/height, and the square size and gap that will be set between each square.
6. So if we now have positions, shape and colors, we can continue with declaring the actual defs that will: draw_square
