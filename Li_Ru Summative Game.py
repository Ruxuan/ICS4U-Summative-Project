_author_="Li,Ru"
_date_="Wednesday, Jan 23rd, 2012"
_version_="2.0"
_filename_="Summative Assignment Game"
_description_="Sneaking Game based off of Ultimate Assassin by games121.com"


#Version 2:
#- Added comments
#- Fixed up errors

#Things not implemented because of time:
#- When guards notice objective is dead or missing, it does not trigger
#  alert phase
#- Guards don't get knocked out 
#- Nothing different during alert phase
#- No Walls, bushes, environment

#Things that don't work:
#- Everything in the game right now SHOULD work

# Circle-Circle intersection math. Very helpful websites.
#http://stackoverflow.com/questions/3349125/circle-circle-intersection-points
#http://mathworld.wolfram.com/Circle-CircleIntersection.html

from tkinter import *
import random
import math

def create_grid(canvas):
    """Creates a basic grid for the map. 20 by 20 squares"""
    rows = 28
    cols = 49
    sq = 20
    margin = 10
    for a in range(rows):
        y0 = a*sq+margin
        y1 = a*sq+margin+sq
        for b in range(cols):
            x0 = b*sq+margin
            x1 = b*sq+margin+sq
            canvas.create_rectangle(x0,y0,x1,y1,fill="white")
            
class Player():
    """Player Class"""
    #Speed and color
    speed = 3
    color = "Black"
    def __init__(self, canvas, tag, energy , health , x=0, y=0):
        """Constructor"""
        self.canvas = canvas
        self.tag = tag
        self.x = x
        self.y = y
        self.energy = energy
        self.health = health
        self.redraw()
        
    def move_up(self):
        """move up method for player"""
        self.y = self.y - Player.speed
    def move_down(self):
        """move down method for player"""
        self.y = self.y + Player.speed
    def move_right(self):
        """move right method for player"""
        self.x = self.x + Player.speed
    def move_left(self):
        """move left method for player"""
        self.x = self.x - Player.speed

    def health_loss(self):
        """Method for player losing health"""
        if self.health > 0:
            self.health -= 1
    def energy_loss(self):
        """Method for player losing energy"""
        if self.energy > 0:
            self.energy -= 1
        
    def energy_regen(self):
        """Method for player regenerating energy"""
        if self.energy < 100:
            self.energy += 0.5

    def detection(self,guard_z):
        """Detection method checks if the guard can see the player"""
        #Detection explaination is in the word file
        d = math.sqrt((self.x - guard_z.x)*(self.x - guard_z.x)+(self.y - guard_z.y)*(self.y - guard_z.y))
        total_radius = Guards.vision_range + 10
        
        if d <= total_radius and d > 10:
            sector = int(20 * round(float(d)/20))
            a = int(((sector*sector)-(10*10)+(d*d))/(2*d))
            h = math.sqrt(sector*sector - a*a)

            midx = guard_z.x + a*(self.x-guard_z.x)/d
            midy = guard_z.y + a*(self.y-guard_z.y)/d

            x0 = midx + h*(self.y-guard_z.y)/d
            x1 = midx - h*(self.y-guard_z.y)/d
            y0 = midy - h*(self.x-guard_z.x)/d
            y1 = midy + h*(self.x-guard_z.x)/d
            
            if guard_z.path[guard_z.counter] == "up":
                if guard_z.x-sector*math.sin(math.radians(40)) < x0 < guard_z.x+sector*math.sin(math.radians(40)) or guard_z.x-sector*math.sin(math.radians(40)) < x1 < guard_z.x+sector*math.sin(math.radians(40)):
                    if guard_z.y-sector*math.cos(math.radians(40)) > y0 > guard_z.y-sector or guard_z.y-sector*math.cos(math.radians(40)) > y1 > guard_z.y-sector:
                        guard_z.detection = True
                        status["detected"] = True
            elif guard_z.path[guard_z.counter] == "left":
                if guard_z.x-sector*math.cos(math.radians(40)) > x0 > guard_z.x-sector or guard_z.x-sector*math.cos(math.radians(40)) > x1 > guard_z.x-sector:
                    if guard_z.y-sector*math.sin(math.radians(40)) < y0 < guard_z.y+sector*math.sin(math.radians(40)) or guard_z.y-sector*math.sin(math.radians(40)) < y1 < guard_z.y+sector*math.sin(math.radians(40)):
                        guard_z.detection = True
                        status["detected"] = True
            elif guard_z.path[guard_z.counter] == "right":
                if guard_z.x+sector*math.cos(math.radians(40)) < x0 < guard_z.x+sector or guard_z.x+120*math.cos(math.radians(40)) < x1 < guard_z.x+sector:
                    if guard_z.y+sector*math.sin(math.radians(40)) > y0 > guard_z.y-sector*math.sin(math.radians(40)) or guard_z.y+sector*math.sin(math.radians(40)) > y1 > guard_z.y-sector*math.sin(math.radians(40)):
                        guard_z.detection = True
                        status["detected"] = True
            elif guard_z.path[guard_z.counter] == "down":
                if guard_z.x+sector*math.sin(math.radians(40)) > x0 > guard_z.x-sector*math.sin(math.radians(40)) or guard_z.x+sector*math.sin(math.radians(40)) > x1 > guard_z.x-sector*math.sin(math.radians(40)):
                    if guard_z.y+sector*math.cos(math.radians(40)) < y0 < guard_z.y+sector or guard_z.y+sector*math.cos(math.radians(40)) < y1 < guard_z.y+sector:
                        guard_z.detection = True
                        status["detected"] = True
            else:
                #Explaination in word document for when the guard is scanning an area
                #is slightly different from the solution below
                
                qcos = math.cos(math.radians(guard_z.path[guard_z.counter]))
                qsin = math.sin(math.radians(guard_z.path[guard_z.counter]))
                qcos80 = math.cos(math.radians(guard_z.path[guard_z.counter]+80))
                qsin80 = math.sin(math.radians(guard_z.path[guard_z.counter]+80))
                
                if 0 <= guard_z.path[guard_z.counter] <= 90:
                    arc_x0 = guard_z.x+sector*qcos80
                    arc_y0 = min(guard_z.y-sector*qsin , guard_z.y-(sector+35)*qsin , guard_z.y-sector*qsin80 , guard_z.y-(sector+35)*qsin80)
                    arc_x1 = guard_z.x+sector*qcos
                    arc_y1 = max(guard_z.y-sector*qsin , guard_z.y-(sector+35)*qsin , guard_z.y-sector*qsin80 , guard_z.y-(sector+35)*qsin80)
                elif 90 < guard_z.path[guard_z.counter] <= 180:
                    arc_x0 = min(guard_z.x+sector*qcos , guard_z.x+(sector+35)*qcos , guard_z.x+sector*qcos80 , guard_z.x+(sector+35)*qcos80)
                    arc_y0 = guard_z.y-sector*qsin
                    arc_x1 = max(guard_z.x+sector*qcos , guard_z.x+(sector+35)*qcos , guard_z.x+sector*qcos80 , guard_z.x+(sector+35)*qcos80)
                    arc_y1 = guard_z.y-sector*qsin80
                elif 180 < guard_z.path[guard_z.counter] <= 270:
                    arc_x0 = guard_z.x+sector*qcos
                    arc_y0 = min(guard_z.y-sector*qsin , guard_z.y-(sector+35)*qsin , guard_z.y-sector*qsin80 , guard_z.y-(sector+35)*qsin80)
                    arc_x1 = guard_z.x+sector*qcos80
                    arc_y1 = max(guard_z.y-sector*qsin , guard_z.y-(sector+35)*qsin , guard_z.y-sector*qsin80 , guard_z.y-(sector+35)*qsin80)
                elif 270 < guard_z.path[guard_z.counter] <= 360:
                    arc_x0 = min(guard_z.x+sector*qcos , guard_z.x+(sector+35)*qcos , guard_z.x+sector*qcos80 , guard_z.x+(sector+35)*qcos80)
                    arc_y0 = guard_z.y-sector*qsin80
                    arc_x1 = max(guard_z.x+sector*qcos , guard_z.x+(sector+35)*qcos , guard_z.x+sector*qcos80 , guard_z.x+(sector+35)*qcos80)
                    arc_y1 = guard_z.y-sector*qsin                
                if arc_x0 < x0 < arc_x1 or arc_x0 < x1 < arc_x1:
                    if arc_y0 < y0 < arc_y1 or arc_y0 < y1 < arc_y1:
                        guard_z.detection = True
                        status["detected"] = True
                        
    def edge_restrictions(self):
        """Restricts the player from moving off the map"""
        self.x = min(980,self.x)
        self.x = max(20,self.x)
        self.y = min(560,self.y)
        self.y = max(20,self.y)

    def redraw(self):
        """The redraw function for Player"""
        self.edge_restrictions()
        
        x0 = self.x - 10
        x1 = self.x + 10
        y0 = self.y - 10
        y1 = self.y + 10
        
        e_bar = (990 - self.energy*3)
        h_bar = 10 + self.health*3
        
        self.canvas.delete(self.tag)
        self.canvas.delete("e")
        self.canvas.delete("h")
        self.canvas.create_oval(x0,y0,x1,y1,tags=self.tag,fill=Player.color, outline="Black")
        self.canvas.create_rectangle(e_bar,575,990,590,tag="e",fill="yellow")
        self.canvas.create_rectangle(10,590,h_bar,575,tag="h",fill="red")

class Guards():
    """Guards Class"""
    #Vision range and move speed would've both increasesd when in alert phase but I ran out of time for the code for that.
    vision_range = 120
    move_speed = 2
    def __init__(self, canvas, x, y, tag, route="rand"):
        """Guard Class' Constructor"""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.tag = tag
        self.vision_tag = self.tag+"_vision"
        self.route = route
        self.detection = False
        self.path = []
        self.counter = 0

    def move_up(self, direction):
        """move up method for guards"""
        self.y = self.y - Guards.move_speed
        self.redraw(direction)
    def move_down(self, direction):
        """move down method for guards"""
        self.y = self.y + Guards.move_speed
        self.redraw(direction)
    def move_right(self, direction):
        """move right method for guards"""
        self.x = self.x + Guards.move_speed
        self.redraw(direction)
    def move_left(self, direction):
        """move left method for guards"""
        self.x = self.x - Guards.move_speed
        self.redraw(direction)

    def edge_restrictions(self):
        """edge restriction so guards don't go off the map"""
        self.x = min(980,self.x)
        self.x = max(20,self.x)
        self.y = min(560,self.y)
        self.y = max(20,self.y)
       
    def knock_out(self):
        """Deletes guards after they're knocked unconscious"""
        self.canvas.delete(self.tag)

    def look_at_player(self):
        """Once detected, guards will look directly at the player"""
        # h = Hypotenuse
        # a = Adjacent
        # cos = a/h
        # acos(a/h) = s
        
        h = math.sqrt((unit.x - self.x)*(unit.x - self.x)+(unit.y - self.y)*(unit.y - self.y))
        a = abs(unit.x - self.x)
        s = math.degrees(math.acos(a/h))
        if self.x >= unit.x:
            if self.y >= unit.y:
                detect_start = 180-s
            if self.y <= unit.y:
                detect_start = s+180
        if self.x <= unit.x:
            if self.y >= unit.y:
                detect_start = s
            if self.y <= unit.y:
                detect_start = 360-s
        detect_start -= 40
        self.redraw(detect_start)
        
    def attack_player(self):
        """Draws the bullet when player is spotted by guards"""
        self.canvas.create_line(self.x,self.y,unit.x,unit.y, fill = "yellow", tag = "shot")
        
    def redraw(self, direction):
        """Redraw for guards"""
        self.edge_restrictions()

        if direction == "up":
            self.start = 50
        elif direction == "left":
            self.start = 140
        elif direction == "right":
            self.start = 320
        elif direction == "down":
            self.start = 230
        else:
            self.start = direction
    
        self.canvas.delete(self.vision_tag)
        self.canvas.create_arc(self.x-Guards.vision_range,self.y-Guards.vision_range,self.x+Guards.vision_range,self.y+Guards.vision_range,start = self.start, extent = 80,tag=self.vision_tag,fill="#F08080",outline="#F08080")
        
        x0 = self.x - 10
        x1 = self.x + 10
        y0 = self.y - 10
        y1 = self.y + 10
        
        self.canvas.delete(self.tag)
        self.canvas.create_oval(x0,y0,x1,y1,tag=self.tag,fill="blue")
                    
    def rand_route(self):
        """Set guards to random route"""
        ran_direction = random.randint(1,6)
        ran_distance = random.randint(1,90)

        if ran_direction == 5:
            self.look_around()
        else:
            for x in range(ran_distance):
                if ran_direction == 1:
                    self.path.append("down")
                if ran_direction == 2:
                    self.path.append("up")
                if ran_direction == 3:
                    self.path.append("left")
                if ran_direction == 4:
                    self.path.append("right")
                self.path.append("False")
        
    def look_around(self):
        """Method for guards to look around them"""
        start = random.randint(0,360)
        extent = random.randint(90,270)
        turn = random.randint(1,2)
        if turn == 1:
            for x in range(extent):
                if start+x >= 360:
                    self.path.append(int(start+x-360))
                else:
                    self.path.append(int(start+x))
        if turn == 2:
            for x in range(extent):
                if start-x <= 0:
                    self.path.append(int(360+start-x))
                else:
                    self.path.append(int(start-x))
        self.path.append("False")
                        
    def m1_route_one(self):
        """map 1, route one"""
        for x in range(60):
            self.path.append("down")
        for x in range(60):
            self.path.append("right")
        for x in range(60):
            self.path.append("up")
        for x in range(60):
            self.path.append("left")
        self.path.append("False")

    def m1_route_two(self):
        """map 1, route_two"""
        for x in range(50):
            self.path.append("right")
        for x in range(50):
            self.path.append("down")
        for x in range(25):
            self.path.append("left")
        for x in range(25):
            self.path.append("up")
        for x in range(25):
            self.path.append("left")
        for x in range(25):
            self.path.append("up")
        self.path.append("False")

class Objective():
    """Objective Class"""
    def __init__(self,canvas,x,y,tag,killed):
        """Constructor"""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.counter = 0
        self.path = []
        self.killed = False
        self.tag = tag
        if tag == "Objective":
            self.rand_route()
        self.redraw()
        
    def move_up(self):
        """move up method for Objectives"""
        self.y = self.y - 2
        self.redraw()
    def move_down(self):
        """move down method for Objectives"""
        self.y = self.y + 2
        self.redraw()
    def move_right(self):
        """move right method for Objectives"""
        self.x = self.x + 2
        self.redraw()
    def move_left(self):
        """move left method for Objectives"""
        self.x = self.x - 2
        self.redraw()

    def stop(self):
        """Target is killed if player is nearby"""
        if self.x - 10 < unit.x < self.x + 10:
            if self.y - 10 < unit.y < self.y + 10:
                self.killed = True

    def escape(self):
        """Player escapes if nearby the hole"""
        if 30-10 < unit.x < 30+10:
            if 30-10 < unit.y < 30+10:
                status["gamewin"] = True
        
    def edge_restrictions(self):
        """Edge restrictions to prevent objective from going off screen"""
        self.x = min(980,self.x)
        self.x = max(20,self.x)
        self.y = min(560,self.y)
        self.y = max(20,self.y)
        
    def redraw(self):
        """Redraw method for objective"""
        self.edge_restrictions()
        if self.killed == False:
            color = "Green"
        elif self.killed == True:
            color = "Red"
        if self.tag == "Escape":
            color = "#C0C0C0"
            
        x0 = self.x - 10
        x1 = self.x + 10
        y0 = self.y - 10
        y1 = self.y + 10
        
        self.canvas.delete(self.tag)
        self.canvas.create_oval(x0,y0,x1,y1,tag=self.tag,fill = color)
       
    def rand_route(self):
        """Random route for objective"""
        ran_direction = random.randint(1,5)
        ran_distance = random.randint(1,90)
        
        for x in range(ran_distance):
            if ran_direction == 1:
                self.path.append("down")
            if ran_direction == 2:
                self.path.append("up")
            if ran_direction == 3:
                self.path.append("left")
            if ran_direction == 4:
                self.path.append("right")
        self.path.append("False")
        
class Map:
    """Map Class"""
    @staticmethod
    def map_one():
        """Level one"""
        guards.append(Guards(canvas,600,400,"g1","m1r1"))
        guards.append(Guards(canvas,800,200,"g2","m1r2"))
        guards.append(Guards(canvas,400,400,"g4","rand"))
        guards.append(Guards(canvas,300,200,"g3","scan"))
        guards[0].m1_route_one()
        guards[1].m1_route_two()
        guards[2].rand_route()
        guards[3].look_around()
        objective.append(Objective(canvas,950,550,"Objective",False))
        objective.append(Objective(canvas,30,30,"Escape",True))
        
def setup():
    """setup game"""
    status["detected"] = False
    status["gameover"] = False
    status["pause"] = False
    status["objective"] = False
    status["gamewin"] = False
    canvas.create_rectangle(MINX,MINY,MAXX,MAXY)
    for x in ["Up","Down","Right","Left","z","x","p"]:
        root.bind("<KeyPress-%s>" % x, pressed)
        root.bind("<KeyRelease-%s>" % x, released)
        press[x] = False
    root.bind("p",paused)
    create_grid(canvas)
        
def animate():
    """Main loop for Game"""
    #Pause game
    if status["pause"] == True:
        canvas.after(20, animate)
    elif status["gameover"] == False and status["gamewin"] == False:
        if unit.health == 0:
            status["gameover"] = True
            
        canvas.delete("shot")#removes the bullet shot lines after player breaks line of sight

        #checks special player skills
        if press["z"] == False and press["x"] == False:
            unit.energy_regen()

        if press["z"] == True and unit.energy > 0:
            Player.speed = 6
            unit.energy_loss()
        else:
            Player.speed = 3
        if press["x"] == True and unit.energy > 0:
            Player.color = "White"
            unit.energy_loss()
        else:
            Player.color = "Black"
            
        if Player.color == "Black":
            if press["Up"]:
                unit.move_up()
            if press["Down"]:
                unit.move_down()
            if press["Right"]:
                unit.move_right()
            if press["Left"]:
                unit.move_left()
        #checks detection               
        for z in range(len(guards)):
            #Guards move by reading their path list
            #When the element in the path list is false, it means
            #that the list is done
            #Program then clears and refills the list
            if guards[z].path[guards[z].counter] == "False":
                guards[z].counter = 0
                guards[z].path = []
                if guards[z].route == "rand":
                    guards[z].rand_route()
                elif guards[z].route == "m1r1":
                    guards[z].m1_route_one()
                elif guards[z].route == "m1r2":
                    guards[z].m1_route_two()
                elif guards[z].route == "scan":
                    guards[z].look_around()
            # Only go check detection if player isn't in invisiblity skill
            # Player goes white when invisiblity is activated
            if Player.color == "Black":
                unit.detection(guards[z])
            # When play is detected:
            if guards[z].detection == True:
                guards[z].detection = False
                guards[z].look_at_player()
                guards[z].attack_player()
                unit.health_loss()
            # Movement
            elif guards[z].path[guards[z].counter] != "False":
                if guards[z].path[guards[z].counter] == "down":
                    guards[z].move_down(guards[z].path[guards[z].counter])
                elif guards[z].path[guards[z].counter] == "up":
                    guards[z].move_up(guards[z].path[guards[z].counter])
                elif guards[z].path[guards[z].counter] == "right":
                    guards[z].move_right(guards[z].path[guards[z].counter])
                elif guards[z].path[guards[z].counter] == "left":
                    guards[z].move_left(guards[z].path[guards[z].counter])
                else:
                    guards[z].redraw(guards[z].path[guards[z].counter])
                guards[z].counter += 1
        # Objective movement
        # if objective is killed, he stops moving and color becomes red
        # Only after objective has been killed, can you move to the exit point
        for x in range(2):
            if objective[x].killed == False:
                objective[x].stop()
                if objective[x].tag == "Objective":
                    if objective[x].path[objective[x].counter] == "False":
                        objective[x].counter = 0
                        objective[x].path = []
                        if objective[x].tag == "Objective":
                            objective[x].rand_route()
                    else:
                        if objective[x].path[objective[x].counter] == "down":
                            objective[x].move_down()
                        elif objective[x].path[objective[x].counter] == "up":
                            objective[x].move_up()
                        elif objective[x].path[objective[x].counter] == "right":
                            objective[x].move_right()
                        elif objective[x].path[objective[x].counter] == "left":
                            objective[x].move_left()
                        objective[x].counter += 1
            else:
                objective[x].redraw()
                if objective[0].killed == True:
                    objective[1].escape()
        unit.redraw()
        canvas.after(20, animate)
    else:
        #game finishes
        my_font = ("arial",80,"bold")
        if status["gameover"] == True:
            canvas.create_text(400,300,text = "LOSE", font = my_font)
        elif status["gamewin"] == True:
            canvas.create_text(400,300,text = "WIN", font = my_font)

def paused(event):
    """Pause game"""
    if status["pause"] == True:
        status["pause"] = False
    else:
        status["pause"] = True
def pressed(event):
    """Pressed True"""
    press[event.keysym] = True
def released(event):
    """Released False"""
    press[event.keysym] = False

press = {}
guards = []
status = {}
objective = []

root = Tk()
canvas = Canvas(root, width = 1000, height = 600)
root.title("ICS4U Game RU LI")
canvas.pack()

MAXX = 990
MINX = 10
MAXY = 570
MINY = 10

setup()

unit = Player(canvas, tag="p1", energy=100, health=100, x=100, y=100)

Map.map_one()

animate()

root.mainloop()
