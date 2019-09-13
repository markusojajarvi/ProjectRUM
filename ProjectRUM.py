import mysql.connector
from tkinter import *
from time import sleep, monotonic
from random import randint, shuffle
from winsound import *

db = mysql.connector.connect(host='localhost',
                             user='dbuser09',
                             passwd='dbpass',
                             db='projectrum',
                             buffered=True)
cur = db.cursor()

def planks():
    if loc==3:
        cur.execute("SELECT COUNT(*) FROM item WHERE location_id = 3")
        count = cur.fetchall()[0][0]
        if count==2:
            update_image(plank2)
        elif count==1:
            update_image(plank1)
        else:
            update_image(images[3])
            cur.execute("UPDATE move SET tolocation_id = 3 WHERE location_id = 5 and direction = 'north'")
            cur.execute("UPDATE move SET tolocation_id = 4 WHERE location_id = 3 and direction = 'south'")

PlaySound('audio/start.wav', SND_ASYNC)
def audio(loc):
    cur.execute("SELECT location_id FROM npc WHERE name = 'dog'")
    result = cur.fetchall()[0][0]
    global village
    if loc==0:
        PlaySound('audio/start.wav', SND_ASYNC)
    elif loc==1 or loc==3 or loc==13:
        PlaySound('audio/beach.wav', SND_ASYNC)
    elif loc==6 and not dogkey and result==6:
        PlaySound('audio/doge.wav', SND_ASYNC)
    elif loc==6 or loc==7 or loc==8 or loc==15:
        PlaySound('audio/jungle.wav', SND_ASYNC)
    elif loc==4 or loc==5 or  loc==16 or loc==17:
        PlaySound('audio/cave.wav', SND_ASYNC)
    elif loc==11 and not village:
        PlaySound('audio/village.wav', SND_ASYNC)
    elif loc==2:
        PlaySound('audio/hut.wav', SND_ASYNC)
    elif loc==14:
        PlaySound('audio/graveyard.wav', SND_ASYNC)
    elif loc==13:
        PlaySound('audio/machete.wav', SND_ASYNC)
    elif loc==9:
        PlaySound('audio/golden.wav', SND_ASYNC)
    elif loc==-2:
        PlaySound('audio/fail.wav', SND_ASYNC)
    elif loc==-1:
        PlaySound('audio/victory.wav', SND_ASYNC)
    elif loc==10:
        PlaySound('audio/hangman.wav', SND_ASYNC)

def location():
    cur.execute("SELECT location_id FROM player")
    global loc
    loc = cur.fetchall()[0][0]

location()

def update_location(new_loc):
    global loc
    loc = new_loc
    sql = "UPDATE player SET location_id = "+str(loc)+" WHERE player_id = 1"
    cur.execute(sql)
    if loc==666:
        new_loc = -2
    elif loc==1001:
        new_loc = -1
    update_image(images[new_loc])
    audio(new_loc)

def look():
    location()
    global loc
    cur.execute("SELECT description FROM location WHERE location_id ="+str(loc))
    txt1 = cur.fetchall()[0][0]

    # Items on the ground
    sql = "SELECT name FROM itemtype INNER JOIN item ON item.type_id = itemtype.type_id WHERE location_id = "+str(loc)
    cur.execute(sql)
    result = cur.fetchall()
            
    if result:
        # deal with the duplicates (copied from interwebs so not 100% sure how it works)
        no_dupes = [x for n, x in enumerate(result) if x not in result[:n]]
        dupes = [x for n, x in enumerate(result) if x in result[:n]]

        result = no_dupes

        # Form text
        txt = ""
        for i in result:
            txt += fullname(i[0],True)
            if i in dupes:
                txt += "s"
                
            if len(result) >= 2 and i == result[-2]:
                txt += " and "
            elif i != result[-1]:
                txt += ", "
            

        # e.g. 'item' " sticks out from the white sand."
        cur.execute("SELECT additive FROM location WHERE location_id ="+str(loc))
        result2 = cur.fetchall()[0][0]
        if result2 != None:
            additive = result2
        else:
            additive = "{0} lay{1} on the ground."

        if len(result)+len(dupes)>1:
            many = ""
        else:
            many = "s"

        update_text(txt1 + " " + additive.format(txt, many).capitalize())
    else:
        update_text(txt1)

    dog()
    golden_city()
    if loc==11 and coco < 1:
        update_text("# Coconut man: Hello umm.. friend. Do you happen to have any coconuts? I need them for my umm.. experiment. #",start="")
    elif loc==12:
        shop_inv()
    elif loc==3:
        update_text("# Jeff: There's \""+graffiti+"\" written with blood on the wall next to the entrance. #",start="")


def graffiti_maker():
    nums = list(str(root))
    chars = list(word)
    graf = nums+chars
    shuffle(graf)
    return ''.join(graf)

village = False

def move(d):
    global village
    if loc==3 and d=="south":
        cur.execute("SELECT item_id FROM itemtype INNER JOIN item ON item.type_id = itemtype.type_id WHERE player_id = 1 AND item.type_id = 11")
        if cur.fetchall():
            cur.execute("UPDATE move SET tolocation_id = 5 WHERE location_id = 3 and tolocation_id = 4")
        else:
            cur.execute("UPDATE move SET tolocation_id = 4 WHERE location_id = 3 and tolocation_id = 5")
            
    elif loc==15 and d=="south":
        cur.execute("SELECT item_id FROM itemtype INNER JOIN item ON item.type_id = itemtype.type_id WHERE player_id = 1 AND item.type_id = 11")
        if cur.fetchall():
            cur.execute("UPDATE move SET tolocation_id = 17 WHERE location_id = 15 and tolocation_id = 16")
        else:
            cur.execute("UPDATE move SET tolocation_id = 16 WHERE location_id = 15 and tolocation_id = 17")

    elif loc==11 and d=="north":
        village = True
    elif loc==14 and d=="north":
        village = False
    elif loc==6 and d=="west":
        village = False
    elif loc==7 and d=="west":
        village = False
            
    sql = 'SELECT tolocation_id,locked FROM move WHERE location_id='+str(loc)+' AND direction="'+d+'"'
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        if result[0][0]:
            update_location(result[0][0])
            look()
        else:
            update_text(result[0][1])
    else:
        update_text("# Jeff: I can't go that way. #")

def die(new_loc = 666):
    db.rollback() # RESET
    if new_loc==1001:
        time = int(monotonic() - start_time)
        update_text("Your time: "+str(time)+" seconds.",start="\n")
        cur.execute("SELECT seconds FROM record")
        record = cur.fetchall()[0][0]
        if time > record:
            update_text("NEW RECORD !!!",start=" ")
            cur.execute("UPDATE record SET seconds = "+str(time))
            db.commit()
        else:
            update_text("Record is "+record+" seconds.",start=" ")
    update_location(new_loc)
    update_text("*** PRESS ENTER TO RESTART ***", start="\n\n")

def combine(*ing):
    if len(ing[0]) > 4:
        update_text("# Jeff: I only got two hands and legs. #")
        return
    c = []
    for i in ing[0]:
        j = check_inv(i)
        if j:
            c.append(str(j[1]))
        else:
            update_text("# Jeff: I am not sure what you mean. #")
            return
            
    if len(c)>=1:        
        if len(c)>=2:
            sql = "SELECT MAX(type_id) FROM recipe WHERE Recipe_id NOT IN (SELECT Recipe_id FROM  ingredients  WHERE type_id NOT IN ({0}))".format(','.join(c))
            cur.execute(sql)
            print(sql)
            result = cur.fetchall()
            if result:
                item = result[0][0]
                if item==11 and (loc in [4,16]):
                    update_location(loc+1)
                cur.execute("INSERT INTO item Values ("+new_item_id()+","+str(item)+",1,null,null)")
                cur.execute("DELETE FROM item WHERE player_id = 1 and type_id = "+c[0]+" LIMIT 1")
                cur.execute("DELETE FROM item WHERE player_id = 1 and type_id = "+c[1]+" LIMIT 1")
                if len(c)>=3:
                    cur.execute("DELETE FROM item WHERE player_id = 1 and type_id = "+c[2]+" LIMIT 1")
                    if len(c)==4:
                        cur.execute("DELETE FROM item WHERE player_id = 1 and type_id = "+c[3]+" LIMIT 1")
                update_text("# Jeff: Done! #")
                PlaySound('audio/craft.wav', SND_ASYNC)
            else:
                update_text("# Jeff: My mom did not teach me that. #")
            return
    update_text("# Jeff: Crafting reguires atleast two items. #")
    

def fullname(item, locate=False):
    sql = "SELECT display_name FROM itemtype INNER JOIN item ON item.type_id = itemtype.type_id WHERE name = '{0}'".format(item)
    if locate:
        sql += " and location_id = "+str(loc)
    cur.execute(sql)
    try:
        result = cur.fetchall()[0][0]
    except:
        result = ""
    if result != "":
        return (result + " " + item)
    else:
        return item
    
def inventory():
    sql = "SELECT itemtype.name, gold FROM itemtype INNER JOIN item ON itemtype.type_id = item.type_id INNER JOIN player ON item.player_id = player.player_id"
    cur.execute(sql)
    result = cur.fetchall()

    # deal with the duplicates (copied from interwebs so not 100% sure how it works)
    no_dupes = [x for n, x in enumerate(result) if x not in result[:n]]
    dupes = [x for n, x in enumerate(result) if x in result[:n]]

    result = no_dupes
    
    money = result[0][1]        
    if cur.rowcount>=1:
        update_text("The following items are in your inventory:")
        if money:
            update_text("- {0} gold ore".format(money),start="\n")
        for row in result:
            if row in dupes:
                update_text(" - " + str(dupes.count(row)+1) + " " + (fullname(row[0])).capitalize(), start="\n")
            else:
                update_text(" - " + (fullname(row[0])).capitalize(), start="\n")
    else:
        update_text("You don't have anything in your inventory.")

def check_loc(item):
    global loc
    sql = "SELECT item_id, item.type_id FROM itemtype INNER JOIN item ON item.type_id = itemtype.type_id WHERE location_id = "+str(loc)
    sql += ' AND name = "'+item+'"'
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0]
    else:
        return 0

def check_inv(item):
    sql = "SELECT item_id, item.type_id FROM itemtype INNER JOIN item ON item.type_id = itemtype.type_id"
    sql += " WHERE player_id = 1"
    sql += ' AND name = "'+item+'"'
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0]
    else:
        return 0

def check_db(item):
    sql = "SELECT item_id FROM itemtype INNER JOIN item ON item.type_id = itemtype.type_id"
    sql += ' WHERE name = "'+item+'"'
    cur.execute(sql)
    result = cur.fetchall()
    if result:
        return result[0][0]
    else:
        return 0

def new_item_id():
    cur.execute("SELECT MAX(item_id)+1 FROM item")
    return str(cur.fetchall()[0][0])

def get(item):
    result = check_loc(item)
    if result:
        item_id = result[0]
        itemtype = result[1]
        if itemtype == 5 and loc == 6:
            # Add a new stick while you take one away
            cur.execute("INSERT INTO item Values ("+new_item_id()+",5,null,6,null)")   

        if item_id == 23:
            PlaySound('audio/pick.wav',SND_ASYNC)
            update_text("Jeff takes the statue of the pedestal. The pedestal moves up slightly as if detecting the statue being removed. On the top of the golden stairs a door way slams open. Before Jeff even realizes what is happening a huge golden boulder rolls down the stair and flattens everything me included.")
            die()
        elif itemtype == 24:
            cur.execute("DELETE FROM item WHERE item_id = "+str(item_id))
            cur.execute("UPDATE player SET gold = gold+1 WHERE player_id = 1")
            update_text("One piece of gold ore added.")
            PlaySound('audio/pick.wav',SND_ASYNC)
        elif itemtype == 25:
            cur.execute("DELETE FROM item WHERE item_id = "+str(item_id))
            cur.execute("UPDATE player SET gold = gold+3 WHERE player_id = 1")
            update_text("Three pieces of gold ore added.")
            PlaySound('audio/pick.wav',SND_ASYNC)
        elif item_id != -1:
            cur.execute("UPDATE item SET location_id = null WHERE item_id = " + str(item_id))
            cur.execute("UPDATE item SET player_id = 1 WHERE item_id = " + str(item_id))
            PlaySound('audio/pick.wav',SND_ASYNC)
            return 1
        else:
            update_text("I can't find "+item+".")

def examine(item):
    sql = "SELECT itemtype.description FROM itemtype INNER JOIN item ON itemtype.type_id = item.type_id INNER JOIN player ON itemtype.name = '"+item+"' and (item.player_id = 1 or item.location_id = "+str(loc)+")"
    cur.execute(sql)
    result = cur.fetchall()[0][0]
    if item=="can" and result=="":
        update_text("# Jeff: I shake the can and a rusty key drops out of it. Before I have time to pick it up a dog runs from out of nowhere and snatches the key and runs into the jungle. #")
        cur.execute("UPDATE itemtype SET description = 'Rusty tin can with nothing inside.' WHERE name = 'can'")
        cur.execute("UPDATE npc SET location_id = 6 WHERE name = 'dog'") # add the dog
    elif result:
        update_text(result)
    else:
        update_text("# Jeff: There's no such item around! #")

def dog():
    cur.execute("SELECT location_id FROM npc WHERE name = 'dog'")
    result = cur.fetchall()[0][0]
    if result==loc:
        global gcity_found
        if loc==6:
            txt = "Dog sits on the opposite side of the opening." #Grammar fixed
            if not gcity_found:
                txt += " It sees Jeff and disapears into the jungle."
                cur.execute("UPDATE npc SET location_id = 7 WHERE name = 'dog'")
            update_text(txt,"\n")

        else:
            if loc==9 or (loc==8 and gcity_found):
                new_loc = 6
            else:
                new_loc = loc+1

            sql = "SELECT direction FROM move WHERE location_id = {0} and tolocation_id = {1}".format(loc, new_loc)
            cur.execute(sql)
            result = cur.fetchall()
            if result:
                way = result[0][0]
            else:
                way = "south"

            update_text("I catch a glimps of dogs tail heading "+way+".","\n")

            sql = "UPDATE npc SET location_id = {0} WHERE name = 'dog'".format(new_loc)
            cur.execute(sql)

def golden_city():
    if loc==9:
        global gcity_found
        gcity_found = True
        cur.execute("UPDATE move SET tolocation_id = 6 WHERE tolocation_id = 9")

def shop_inv():
    sql = "SELECT itemtype.name, cost FROM itemtype INNER JOIN item INNER JOIN shop ON itemtype.type_id = item.type_id and item.shop_id = shop.shop_id"
    cur.execute(sql)
    result = cur.fetchall()

    # deal with the duplicates (copied from interwebs so not 100% sure how it works)
    no_dupes = [x for n, x in enumerate(result) if x not in result[:n]]
    dupes = [x for n, x in enumerate(result) if x in result[:n]]

    result = no_dupes
    
    if cur.rowcount >=1:
        update_text("The shop has the following items to sell: ",start="")
        for row in result:
            if row in dupes:
                update_text((" - " + str(dupes.count(row)+1) + " {0} each costs {1} shiny rock").format(fullname(row[0]).capitalize(),row[1]),"\n")
            else:
                update_text(" - {0} costs {1} shiny rock".format(fullname(row[0]).capitalize(),row[1]),"\n")
    else:
        update_text("I don't have any items.")

def buy(item):
    if loc != 12:
        update_text("# Jeff: There is nothing to buy here. #")
    else:
        cur.execute("SELECT cost FROM item INNER JOIN itemtype ON item.type_id = itemtype.type_id WHERE shop_id = 1 and name = '{0}'".format(item))
        result = cur.fetchall()
        if result:
            cur.execute("SELECT gold FROM player")
            if result[0][0] <= cur.fetchall()[0][0]:
                cur.execute("UPDATE player SET gold = gold-"+ str(result[0][0]) +" WHERE player_id = 1")
                cur.execute("UPDATE shop SET gold = gold+"+ str(result[0][0]) +" WHERE shop_id = 1")
                cur.execute("SELECT item_id FROM item INNER JOIN itemtype ON item.type_id = itemtype.type_id WHERE name = '{0}' and shop_id = 1 ORDER BY item_id LIMIT 1".format(item))
                result = cur.fetchall()[0][0]
                cur.execute("UPDATE item SET shop_id = null WHERE item_id = {0}".format(str(result)))
                cur.execute("UPDATE item SET player_id = 1 WHERE item_id = {0}".format(str(result)))
                if item=="rum":
                    cur.execute("INSERT INTO item Values ("+new_item_id()+",9,null,null,1)")
                    update_text("# Shop keeper: There you go and if you need more I got you covered. #")
                else:
                    update_text("# Shop keeper: There you go. #")
            else:
                update_text("# Shop keeper: Your pouch is too light. #")
        else:
            update_text("# Shop keeper: I don't currently have " + item + " but you can view my inventory on the left to see if there's something else you may like. #")

def sell(item):
    if loc != 12:
        update_text("# Jeff: There is no one to sell to. #")
    else:
        cur.execute("SELECT cost FROM item INNER JOIN itemtype ON item.type_id = itemtype.type_id WHERE player_id = 1 and name = '{0}'".format(item))
        result = cur.fetchall()
        if result:
            cur.execute("SELECT gold FROM shop")
            if result[0][0] <= cur.fetchall()[0][0]:
                update_text("# Shop keeper: I am happy to take that from you. #")
                cur.execute("UPDATE player SET gold = gold+"+ str(result[0][0]) +" WHERE player_id = 1")
                cur.execute("UPDATE shop SET gold = gold-"+ str(result[0][0]) +" WHERE shop_id = 1")
                cur.execute("SELECT item_id FROM item INNER JOIN itemtype ON item.type_id = itemtype.type_id WHERE name = '{0}' and player_id = 1 ORDER BY item_id LIMIT 1".format(item))
                result = cur.fetchall()[0][0]
                cur.execute("UPDATE item SET shop_id = 1 WHERE item_id = {0}".format(str(result)))
                cur.execute("UPDATE item SET player_id = null WHERE item_id = {0}".format(str(result)))
            else:
                update_text("# Shop keeper: I am sorry but the price is too steep. #")
        else:
            update_text("# Shop keeper: I would buy it but you don't even have it. #")


# player name
cur.execute("SELECT name FROM player")
name = cur.fetchall()[0][0]

root = Tk()
root.title("Project R.U.M")
root.iconbitmap(r'images/logo.ico')

pw = PanedWindow(root, orient = VERTICAL)
pw.pack()

# All images pre-loaded
cur.execute("SELECT name FROM location")
loc_names = cur.fetchall()
loc_names = [loc_names[i][0] for i in range(len(loc_names))]
images = [PhotoImage(file = "images\\"+name+".png") for name in loc_names]
plank2 = PhotoImage(file = "images\\plank2.png")
plank1 = PhotoImage(file = "images\\plank1.png")
drunk = PhotoImage(file = "images\\Drunk.png")


# Top pane: image
label = Label(image = images[loc])
pw.add(label)

# Middle pane: text output
frame = Frame(height = 200)
frame.pack_propagate(0)

scrollbar = Scrollbar(frame)
text = Text(frame, font=("Courier New", 14))
scrollbar.pack(side = RIGHT, fill = Y)
text.pack(side = LEFT, fill = Y)
scrollbar.config(command = text.yview)
text.config(yscrollcommand = scrollbar.set)

pw.add(frame)

# Bottom pane: text input
command = StringVar()
e = Entry(textvariable = command, font=("Courier New", 14))
e.pack()
e.focus_set()
hangman_on = False
def do(self):
    global loc, hangman_on, radio
    if hangman_on == False and loc == 10: #loc = hangman
        hangman_on = True
        update_text("Cannibals knock Jeff out and when Jeff wakes up he realises that he is about to get hanged.")
        update_text("Guess the word:",start="\n\n")
        for i in hiddenword:
            update_text(i,start=" ")
    elif hangman_on:
        hang = hangman(command.get().lower())
        if hang==1:
            hangman_on = False
            update_text("You got the word right and the cannibals seem confused but cut you down anyways.")
            update_location(11)
            cur.execute("UPDATE move SET tolocation_id = 11 WHERE location_id = 7 and direction = 'west'")
            cur.execute("INSERT INTO item Values ("+str(new_item_id())+",7,1,null,null)")
        elif hang==2:
            hangman_on = False
            update_text('Cannibals laugh and yell "Ooga ooga!!" \n Jeff feels weightless for a split second until his neck breaks.')
            die()
    elif loc==13 and 666 > radio >= 1:
        radio_game(command.get())
    else:
        loop(command.get())
    e.delete(0, END)

e.bind("<Return>", do) # Does "do"-method if enter is pressed

pw.add(e)

# Wait for the image to show before continuing
label.wait_visibility(root)

# Leos text formatter with quite a few changes and some more changes
def form(text):
    splitted = text.split(" ")
    rowlength = 57
    used = 0
    formatter = ""
    bubble = 0
    for word in splitted:
        if word == "#":
            if not bubble:
                bubble = 1
            else:
                bubble = 0
            formatter += "\n"
            used = 0
        elif bubble == 1:
            formatter += word + " "
            used += len(word) + 1
            if word[-1]==':':
                bubble = used
        else:
            left = rowlength - used - len(word)
            if left > 0:
                used += len(word) + 1
                formatter += word + " "
            else:
                formatter += "\n"
                formatter += " " * bubble + word + " "
                used = bubble + len(word) + 1
    return formatter

# Update image and text
def update_image(image):
    label.configure(image = image)
    label.update_idletasks()

def update_text(txt, start = "\n"*10):
    txt = form(txt)
    text.config(state=NORMAL)
    #text.delete(1.0, END) # Clear text
    text.insert(END, start + txt)
    text.config(state=DISABLED)
    text.see(END)
    text.update_idletasks()

def at_start():
    look()
    update_text("*** PRESS ENTER TO START ***", start="\n")

at_start()

def hangman(guess):
    if guess == "skip":
        return 1
    TOTAL = 5
    global total_count, correct_count

    if total_count < TOTAL - 1:
        wordapart = list(word)

        if len(guess)==1:
            correct = True
            for i in range(len(word)):
                if guess==wordapart[i] and hiddenword[i]=="_":
                    hiddenword[i]=guess.upper()
                    correct = False
                    correct_count+=1
                    if correct_count==len(word):
                        return 1
            if correct:
                total_count+=1
        else:
            if guess==word:
                return 1
            else:
                total_count+=1
    else:
        return 2
    
    left = TOTAL-total_count
    if left==TOTAL-1:
        update_text("There's five ropes preventing Jeff from hanging. Cannibals cut one of the ropes. Rope around Jeff's neck tightens.")
    elif left==TOTAL-2:
        update_text("Second rope is cut and three ropes are left holding the gate under Jeff's feet.")
    elif left==TOTAL-3:
        update_text("Third rope snaps under the pressure before the blade even hits it.")
    elif left==TOTAL-4:
        update_text("One rope left. Jeff's life is hanging on a strand LITERALLY.")
    else:
        update_text("")
    
    update_text("Guess the word:",start="\n\n")
    for i in hiddenword:
        update_text(i,start=" ")

    return 0

def radio_game(answer):
    global radio, root
    if radio==1:
        update_text("# Radio: Hello " + answer.capitalize() + "! *static* How can I help you? Over. #")
    elif radio==2:
        for i in answer.split():
            if i in ["stranded","help","save","sos"]:
                update_text("# Radio: You want help from me? Alright... I can help you but you need to answer one more question: What is the squareroot of "+str(root*root)+"? Over. #")
                radio = 2
                break
            else:
                update_text("# Radio: I cannot help you with that. Over. #")
                radio = 666
    elif radio==3:
        if answer==str(root):
            update_text("# Radio: That is correct. I will send you a helicopter but you have to make some signal. Helicopter will land on the marked beach. Over. #")
        else:
            update_text("# Radio: Why are you so brainless. Over. #")
            radio = 666
    if radio==666:
        update_text("# Radio: Static... #",start="\n\n")
        PlaySound('audio/radio.wav', SND_ASYNC)
    else:
        radio+=1
        if radio>=4:
            radio=-1
            


# Words to remove
removable_words = ["and","a","an","the","of","up","at","pina","with","your","palm","&"]
cur.execute('SELECT display_name FROM itemtype WHERE display_name != ""')
result = cur.fetchall()
for j in range(len(result)):
    w = result[j][0].lower().split()
    for i in w:
        if i not in removable_words:
            removable_words.append(i)

def cannot(action, target):
    if target=="":
        update_text("# Jeff: "+action.capitalize()+" what? #")
    elif check_db(target):
        update_text("# Jeff: There's no "+fullname(target)+" in my inventory. #")
    else:
        update_text("# Jeff: I'm afraid I can't "+action+" that. #")

# Use commands
def loop(c):
    # Lowercase
    c = c.lower()

    # Split command into segments
    input_string = c.split()

    # Take out some words
    for i in removable_words:
        while i in input_string and i != input_string[-1]:
            input_string.remove(i)
            
    # First word is action
    if len(input_string)>=1:
        action = input_string[0]
    else:
        action = ""

    # Start and Hell
    if loc==0 or loc==666:
        move("enter")
        # Reset Hangman
        global word, hiddenword, total_count, correct_count
        default_words = open("Hangman words.txt").read().splitlines()
        word = default_words[randint(0,len(default_words)-1)]
        hiddenword = ["_" for i in range(len(word))]
        total_count = correct_count = 0

        # Reset other stuff
        global gcity_found, climbed, digged, coco, radio, root, graffiti, dogkey, village
        gcity_found = climbed = digged = dogkey = village = False
        coco = radio = 0
        root = 10
        while root%10==0:
            root = randint(5,99)
        graffiti = graffiti_maker()

        #time
        global start_time
        start_time = monotonic()

    # combine
    elif action=="combine" or action=="craft" or action=="c":
        combine(input_string[1:])
        
    # second word is target
    else:
        if len(input_string)>=2:
            target = input_string[1]
        else:
            target = ""

        # restart
        if action=="die":
            update_text(name+" can't take it anymore and commits suicide.")
            die()

        # get
        elif (action=="get" or action=="take" or action=="pick") and target!="":
            if target[-1]=="s":
                cur.execute("SELECT COUNT(*) FROM item INNER JOIN itemtype ON item.type_id = itemtype.type_id WHERE name = '{0}' and location_id = {1}".format(target[:-1],loc))
                count = cur.fetchall()[0][0]
                if check_db(target[:-1]):
                    if count>1:
                        for i in range(count):
                            a = get(target[:-1])
                        if a:
                            update_text("{0} {1} picked up.".format(count,fullname(target)).capitalize())
                    else:
                       if get(target[:-1]):
                            update_text("{0} picked up.".format(fullname(target[:-1])).capitalize()) 
                else:
                    cannot(action,target)
            else:
                if check_db(target):
                    if get(target):
                        update_text("{0} picked up.".format(fullname(target)).capitalize())
                else:
                    cannot(action,target)

        # look
        elif (action=="look" or action=="examine" or action=="view"):
            if target=="":
                look()
            elif check_db(target):
                examine(target)

        # inventory
        elif action=="inventory" or action=="i" and target=="":
            inventory()

        # use
        elif action=="use":
            if target=="key" and check_inv(target):
                if loc==1:
                    update_text("Jeff unlocks the door to a small beach hut.")
                    sql="UPDATE move SET tolocation_id = 2 WHERE location_id = 1 AND direction = 'north'"
                    cur.execute(sql)
                else:
                    update_text("# Jeff: There's nothing here to unlock. #")
            elif target=="radio" and check_inv(target) and radio==0:
                if loc==13:
                    update_text("# Radio: Who are you? #")
                    radio = 1
                else:
                    update_text("# Radio: Static... #")
                    PlaySound('audio/radio.wav', SND_ASYNC)
            elif target=="plank" and check_inv(target) and radio==-1:
                if loc==1 or loc==13:
                    update_text("Jeff places planks on the beach. and waits.")
                    for i in range(4):
                        update_text(".",start="")
                        sleep(1.5)
                    if loc==1:
                        update_text("Helicopter lands on the beach next to Jeff. # Pilot: Don't worry I am here to save you. # Jeff nods and enters the helicopter. # Jeff: I will never drink again. #")
                        die(1001) # win
                    else:
                        update_text("Rumbling sound of the helicopter can be heard on the beach. Jeff is smiling. The sound becomes louder every second. But te cannibals have also heard the sound and aren't too happy about it. They come running into the beach and knock Jeff out once more..")
                        die()
            elif target=="pickaxe" and check_inv(target):
                if loc==18:
                    update_text("Jeff mines the raw ore of the wall. # Jeff: I am rich. Whoohoo! # Suddenly the ground shakes and rocks start falling from the roof of the cave. Crushing Jeff under them.")
                    die()
                else:
                    update_text("# Jeff: There's nothing to mine. #")
            elif target=="machete" and check_inv(target):
                if loc==6:
                    update_text("Jeff cuts through the vines like butter.")
                    sql="UPDATE move SET tolocation_id = 11 WHERE location_id = 6 AND direction = 'west'"
                    cur.execute(sql)
                    sql="UPDATE move SET tolocation_id = 6 WHERE location_id = 11 and tolocation_id = 7"
                    cur.execute(sql)
                    PlaySound('audio/machete.wav', SND_ASYNC)
                elif loc ==11:
                    update_text("Jeff cuts through the vines like butter.")
                    sql="UPDATE move SET tolocation_id = 13 WHERE location_id = 11 AND direction = 'west'"
                    cur.execute(sql)
                    PlaySound('audio/machete.wav', SND_ASYNC)
                else:
                    update_text("# Jeff: Cannot use machete here. #")

            elif target=="shovel" and check_inv(target) and not digged:
                if loc==14:
                    update_text("Jeff digs up a fresh smelling grave and uncovers a bone.")
                    cur.execute("INSERT INTO item Values ("+new_item_id()+",14,null,14,null)")
                    digged = True
                else:
                    update_text("# Jeff: There's nothing to shovel. #")
            else:
                cannot(action, target)

        # give bone or give coconut
        elif action=="give":
            cur.execute("SELECT location_id FROM npc WHERE npc_id = 2")
            if loc==6 and cur.fetchall()[0][0]==6:
                if target=="bone" and check_inv(target):
                    update_text("Jeff gives dog the bone and the dog drops the key on the ground.")
                    cur.execute("INSERT INTO item Values ("+new_item_id()+",4,null,6,null)")
                else:
                    update_text("Dog runs away into the jungle.")
                    cur.execute("UPDATE npc SET location_id = 7 WHERE name = 'dog'")
                    
            elif loc==11 and coco!=2:
                if target == "coconuts" and check_inv("coconut"):
                    cur.execute("DELETE FROM item WHERE type_id = 6 and player_id = 1 LIMIT 1")
                    coco += 1
                    target = "coconut"
                if target == "coconut" and check_inv("coconut"):
                    cur.execute("DELETE FROM item WHERE type_id = 6 and player_id = 1 LIMIT 1")
                    coco += 1
                if coco==1:
                    update_text("# Coconut Man: Thank you but I need one more. #")
                elif coco==2:
                    update_text("# Coconut Man: Thank you vey much here take my flint & steel. #")
                    cur.execute("INSERT INTO item Values ("+new_item_id()+",8,1,null,null)")
                
            else:
                cannot(action, target)
                
                
        # drink
        elif action=="drink":
            if check_inv(target) and (target=="rum" or target=="colada"):
                update_text("Jeff drinks every last drop and passes out.")
                sleep(1)
                update_image(drunk)
                PlaySound("audio/colada.wav",SND_ASYNC)
                for i in range(4):
                    sleep(1.5)
                    update_text(".",start="")
                sleep(1.5)
                
                if target == "rum":
                    die(0)
                    at_start()
                else:
                    cur.execute("SELECT item_id FROM item INNER JOIN itemtype ON item.type_id = itemtype.type_id WHERE name = 'colada' and player_id = 1 LIMIT 1")
                    cur.execute("DELETE FROM item WHERE item_id = "+str(cur.fetchall()[0][0]))
                    update_location(1)
                    look()            
            else:
                cannot(action, target)

        # "climb the palm tree with rope"
        elif action=="climb":
            if not climbed:
                if target=="tree" and loc==6:
                    if len(input_string)==3:
                        if input_string[2]=="rope" and check_inv("rope"):
                            update_text("Jeff wraps the rope around the palm tree and climbs to the top. He carefully knocks all three coconuts of the tree and they land on the ground below him. After which Jeff climbs down safely.")
                            cur.execute("INSERT INTO item Values (6,6,null,6,null)")
                            cur.execute("INSERT INTO item Values ("+new_item_id()+",6,null,6,null)")
                            cur.execute("INSERT INTO item Values ("+new_item_id()+",6,null,6,null)")
                            climbed = True
                        elif input_string[2] in ["hands","nothing","palms","arms","none","feet","magic"]: # everything you might be able to try climbing
                            update_text("Jeff scales the palm tree fearlesly and knocks down two coconuts but the third one doesn't budge. Jeff decides to leave it to be safe and slides down but before his feet have time to touch the ground the third coconut falls on his head.")
                            die()
                        else:
                            update_text("# Jeff: I can't do that. #")
                    else:
                        update_text("# Jeff: Climb the palm tree with what? #")
                else:
                    cannot(action, target)
            else:
                update_text("# Jeff: I am not going to do that again. #")

        # move
        elif action=="w" or action=="west" and target=="":
            move("west")
        elif action=="e" or action=="east" and target=="":
            move("east")
        elif action=="n" or action=="north" and target=="":
            move("north")
        elif action=="s" or action=="south" and target=="":
            move("south")

        # shop
        elif action=="buy" and target!="":
            buy(target)
        elif action=="sell" and target!="":
            sell(target)

        # help
        elif action=="help":
            helpwindow = Toplevel()
            helpwindow.title("Help")
            helpwindow.iconbitmap(r'images/logo.ico')
            helpwindow.geometry('%dx%d+0+0' % (600,400))
            helpwindow.resizable(height=False, width=False)
            helpFrame = Frame(helpwindow)
            helpFrame.pack()
            helptext = Text(helpwindow, font=("Courier New", 11))
            helpscrollbar = Scrollbar(helpwindow)
            helpscrollbar.pack(side = RIGHT, fill = Y)
            helpscrollbar.config(command = helptext.yview)
            helptext.config(yscrollcommand = helpscrollbar.set)
            helptext.pack()
            with open('help.txt', 'r') as myfile:
                data = myfile.read()
            helptext.insert(END, data)

        # quit
        elif action=="quit" and target=="":
            update_text("Bye!")
            root.destroy()

        # teleport only for testing !!
        elif action=="tp" and target!="":
            update_location(int(target))

        # not a command
        else:
            update_text("# Jeff: I'm afraid I can't do that. #")
        planks()
