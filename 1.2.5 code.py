import turtle as trtl
import random as rand


times_file_name = "Completion Times.txt"
wn = trtl.Screen()
wn.setup(width=600, height=600) # Give the screen a fixed size
wn.bgcolor("black")
game_running = True #This might be the single most important variable in my entire program


#credits to Google Gemini for assistance with lines 11-27
drawing_turtle = trtl.Turtle()
drawing_turtle.penup()
points = 5
size = 1.8


#draws a spiky star and registers it as an available sprite to use
def draw_spiked_star(drawing_turtle,size,points):
  for _ in range(points):
    drawing_turtle.forward(size)
    drawing_turtle.right(144)


def register_spiked_star(name, size):
  drawing_turtle.begin_poly()
  draw_spiked_star(drawing_turtle,size,points)
  star_polygon = drawing_turtle.get_poly()
  wn.register_shape(name, star_polygon)


wn.tracer(False)
register_spiked_star("spiky_star", 25)


#creates the bricks, turtle, and spikes
def create_objects():
  global bricks, leonardo, spikes, spike_position_list
  spike_position_list = []
  spikes = []
  for step in range(15):
    spike = trtl.Turtle(shape="spiky_star")
    spike.pencolor('red')
    spike.fillcolor('red')
    spike.penup()
    spike.goto(rand.randint(-400,400), rand.randint(-200,300))
    spikes.append(spike)
    spike_position_list.append((spike.xcor(), spike.ycor()))


  bricks = []
  xpositions = [rand.randint(-400,-320), rand.randint(-300,-240), rand.randint(-200,-130), rand.randint(-100,-20), rand.randint(0,60), rand.randint(80,130), rand.randint(150,220), rand.randint(240,300), rand.randint(310,350), rand.randint(360,400)]
  for xcoord in xpositions:
    brick = trtl.Turtle()
    brick.shape("square")
    brick.color("blue")
    brick.shapesize(0.8)
    brick.penup()
    brick.goto(xcoord, rand.randint(-250, 200))
    bricks.append(brick)
   
  leonardo = trtl.Turtle(shape="turtle")
  leonardo.penup()
  leonardo.goto(-500, 0)
  leonardo.shapesize(1.7)
  leonardo.fillcolor("darkgreen")


create_objects()
wn.update() #causes the sprite generation to update instantaneously
wn.tracer(True)


#Text box to write score
scorewriter = trtl.Turtle()
scorewriter.hideturtle()
scorewriter.color("lime green")
scorewriter.penup()
scorewriter.goto(-580, 350)
scorewriter.pendown()
#Text box to write time
timewriter = trtl.Turtle()
timewriter.hideturtle()
timewriter.color("lime green")
timewriter.penup()
timewriter.goto(580,350)
timewriter.pendown()


# Score setup
font_setup = ("Verdana", 25, "normal")
score = 0
elapsed = 0
scorewriter.write(score, font=font_setup)
timewriter.write(elapsed, font=font_setup)
#Time/movement setup
record_delay = 5000
game_over_delay = 7000
move_distance = 3.5
second = 1000


#Controls
def move_forward():
  leonardo.forward(move_distance)
def up_key_pressed():
  leonardo.setheading(90)
def down_key_pressed():
  leonardo.setheading(270)
def redirect():
  leonardo.setheading(0)


#checks if the turtle collided with anything and jumps to the appropriate function
def scores_and_crashes():
  global score, bricks, leonardo, spikes, spike_position_list
  for brick in bricks:
    if brick.isvisible():
      brickcrash_x = abs(leonardo.xcor() - brick.xcor())
      brickcrash_y = abs(leonardo.ycor() - brick.ycor())
      if brickcrash_x < 20 and brickcrash_y < 20:
        brick.hideturtle()
        bricks.remove(brick)
        scorewriter.clear()
        score += 1
        scorewriter.write(score, font=font_setup)
  for spike_x, spike_y in spike_position_list:
    spikecrash_x = abs(leonardo.xcor() - spike_x)
    spikecrash_y = abs(leonardo.ycor() - spike_y)
    if spikecrash_x < 15 and spikecrash_y < 15:
      crashed()
  if score == 10:
    win_condition(times_file_name)
  elif score < 10 and leonardo.xcor() >= 530:
    out_of_bounds_condition()
 
#Marks the turtle as having collided with the spikes.
def crashed():
  global game_running, leonardo, scorewriter
  game_running = False
  scorewriter.clear()
  timewriter.clear()
  leonardo.hideturtle()
  for brick in bricks:
    brick.hideturtle()
  scorewriter.write("Sorry you hit the spikes. You lost.", font=font_setup)
  wn.ontimer(ask_to_play_again, game_over_delay)


def win_condition(file_name):
  global game_running, spikes, leonardo
  game_running = False
  scorewriter.clear()
  timewriter.clear()
  scorewriter.write("Congratulations you hit all of the bricks! You won!", font=font_setup)
  with open(file_name, "a") as times_file:
    times_file.write(str(elapsed) + "\n")
  for spike in spikes:
    spike.hideturtle()
  leonardo.hideturtle()
  wn.ontimer(show_time, record_delay)


def show_time():
  global elapsed
  scorewriter.clear()
  scorewriter.write("You completed the maze in "+str(elapsed)+" seconds.", font=font_setup)
  wn.ontimer(time_record, record_delay)


def out_of_bounds_condition():
  global game_running, spikes, leonardo, bricks
  game_running = False
  for spike in spikes:
    spike.hideturtle()
  for brick in bricks:
    brick.fillcolor('aquamarine')
  scorewriter.clear()
  timewriter.clear()
  leonardo.hideturtle()
  scorewriter.write("Sorry you needed to get all of the bricks. You lost.", font=font_setup)
  wn.ontimer(ask_to_play_again, game_over_delay)


def get_fastest_time(file_name):
#credit to ChatGPT for giving me insight about the try except feature, but the rest is 100% my original code
  try:
    times_file = open(file_name, "r")
    fastest_time = 60
    for line in times_file:
      if int(line) < fastest_time:
        fastest_time = int(line)
    return fastest_time
  except FileNotFoundError:
    return 60


def time_record():
  fastest_time = get_fastest_time(times_file_name)
  if elapsed == fastest_time:
    scorewriter.clear()
    scorewriter.write("Congratulations you got the new high score, you're amazing!", font=font_setup)
  elif fastest_time >= 60:
    scorewriter.clear()
    scorewriter.write()("I believe you can go even faster -- at least under 60 seconds.", font=font_setup)
    print("The fastest time is "+ str(fastest_time) + " seconds.")
  else:
    scorewriter.clear()
    scorewriter.write("You're great at this, you'll break the record soon!", font=font_setup)
    print("The fastest time is "+ str(fastest_time) + " seconds.")
  #jumps to the play again function after 5 seconds
  wn.ontimer(ask_to_play_again, game_over_delay)


def ask_to_play_again():
  wn.onkeypress(None, 'r')
  scorewriter.clear()
  timewriter.clear()
  scorewriter.write("Would you like to play again? (y or n)", font=font_setup)
  wn.onkeypress(reset_game, 'y')
  wn.onkeypress(end_game, 'n')


def reset_game():
  global score, bricks, leonardo, spikes, game_running, spike_position_list, elapsed
  #ensures that nothing happens when a key is accidentally pressed again, and that the game isn't running
  game_running = False
  wn.onkeypress(None, 'y')
  wn.onkeypress(None, 'n')
  wn.onkeypress(None, 'r')


  leonardo.hideturtle()
  for brick in bricks:
    brick.hideturtle()
  for spike in spikes:
    spike.hideturtle()
 
  score = 0
  elapsed = 0
  scorewriter.clear()
  scorewriter.write(score, font=font_setup)


  wn.tracer(False)
  create_objects()
  wn.update()
  wn.tracer(True)
  game_running = True
  game_loop()
  tick_time()



def tick_time():
  global elapsed, second
  if game_running == True:
    elapsed += 1
    timewriter.clear()
    timewriter.write(elapsed, font=font_setup)
    wn.ontimer(tick_time, second)
 
def end_game():
  global bricks, spikes, game_running
  game_running = False
  wn.onkeypress(None, 'y')
  wn.onkeypress(None, 'n')
  for brick in bricks:
    brick.hideturtle()
  for spike in spikes:
    spike.hideturtle()
  scorewriter.clear()
  scorewriter.write("Ok have a nice day! Feel free to come back some other time!", font=font_setup)


#credits to Gemini for the wn.ontimer feature with delay, allows for smoother transitions during direction changes
def game_loop():
  global game_running
  if game_running == True:
    move_forward()
    scores_and_crashes()
    wn.ontimer(game_loop, 5)
    wn.onkeypress(reset_game, "r")
  else:
    wn.onkeypress(None, 'r') #avoids any reaction by clicking the r button when not supposed to
tick_time() #Calls the function to increment time every second


wn.onkeypress(up_key_pressed, "Up")
wn.onkeypress(down_key_pressed, "Down")
wn.onkeypress(redirect, "Right")
wn.listen() # Starts listening for key presses
game_loop() #starts the game loop for the 1st time


# Starts the turtle graphics event loop
wn.mainloop()

