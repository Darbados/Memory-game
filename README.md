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
6. So if we now have positions, shape and colors, we can continue with declaring the actual defs that are involved in the whole program:
  6.1. draw_square - gets the coordinates of the place where event ( mouse or button ) occured, then based on check if on that place              should be revealed object or not, it draws the revealed icon or a square.
  6.2. draw_board - based on the board_width and board_height it draws the actual bord using the draw_square function
  6.3. draw_select_square - function which job is to draw the black border aroud the square that user thinks to click on.
  6.4. draw_icon - based on what is about to be drawed on the given position it draws the actual icon.
  6.5. get_random_board - by having all the colors and all the forms, it return the array that represents the actual board.
  
  Logistic defs:
  6.6. get_coordinates - returns the position from the top and left side of the square.
  6.7. get_pos - checks if the actual event position is real position for the screen.
  
  In game defs:
  6.8 draw_players - it draws two players ( Player 1 and Player 2 ), shows their current score, the winner ( based on the current score ),                      and which player is about to make a turn.
  6.9 all_revealed - check if all the combinations in the game are reached, i.e. if players have found all the matches, i.e. if the game                        has been won.
  
  Effect defs:
  6.10 start_game_animation - fills the screen with the set surface color, draws the bord, waits 250ms, then with a for loop it reveales                                 all the icons on the board, and after 250ms pause it hides all the icons under squares.
  6.11 game_won_animation - it declares one additional color and uses it and the surface backgroung color and then with a loop with 10                                 iterations it changes the surface color, draws the board, updates the display and waits for 300ms.
  
  
  The cycle ends with new game starting.
  
!!! There is at least one thing that I couldn't make here and it is to show the end winner after the last turn is made. I really do not understand why this logic didn't worked for me, as it is completely working while the players makes their moves, but at the end it just proceeds with the game_won_animation and doesn't show the winner. Pitty. Because of that I've made this silly solution to show the winner based on the last move made.

! Another thing I thought it would be nice to have, is to give the opportunity to declare number of squares in horizontal and vertical. And yes, it has its bad sides as well, like making you enter additional information, and it won't start the game until you enter a legit combination, but I thought that it is a good option as well.

Sources of information while making the task:

1. inventyourowncomputergameswithpython - book that I recently bought, which author is Al Sweigart.
2. Internet with of its recources - Google, Stackoverflow
