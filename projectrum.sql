#DROP DATABASE IF EXISTS projectrum;
CREATE DATABASE projectrum;
USE projectrum;

CREATE user 'dbuser09'@'localhost' IDENTIFIED BY 'dbpass';
GRANT SELECT, INSERT, UPDATE, DELETE ON projectrum.* TO dbuser09@localhost;

DROP TABLE IF EXISTS npc;
DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS move;
DROP TABLE IF EXISTS shop;
DROP TABLE IF EXISTS itemtype;
DROP TABLE IF EXISTS location;
DROP TABLE IF EXISTS record;

CREATE TABLE location
(
  location_id INT NOT NULL,
  name VARCHAR(30),
  description VARCHAR(288),
  additive VARCHAR(288),
  PRIMARY KEY (location_id)
);

CREATE TABLE itemtype
(
  type_id INT NOT NULL,
  cost INT,
  name VARCHAR(30),
  display_name VARCHAR(30),
  description VARCHAR(288),
  consumed BIT DEFAULT 1,
  PRIMARY KEY (type_id)
);

CREATE TABLE shop
(
  shop_id INT NOT NULL,
  name VARCHAR(30),
  gold INT,
  location_id INT NOT NULL,
  PRIMARY KEY (shop_id),
  FOREIGN KEY (location_id) REFERENCES location(location_id)
);

CREATE TABLE move
(
  direction VARCHAR(5) NOT NULL,
  location_id INT NOT NULL,
  tolocation_id INT,
  locked VARCHAR(288),
  PRIMARY KEY (direction,location_id),
  FOREIGN KEY (location_id) REFERENCES location(location_id),
  FOREIGN KEY (tolocation_id) REFERENCES location(location_id)
);

CREATE TABLE recipe
(
  Recipe_id INT NOT NULL,
  type_id INT NOT NULL,
  PRIMARY KEY (Recipe_id),
  FOREIGN KEY (type_id) REFERENCES itemtype(type_id)
);

CREATE TABLE ingredients
(
  Recipe_id INT NOT NULL,
  type_id INT NOT NULL,
  PRIMARY KEY (Recipe_id, type_id),
  FOREIGN KEY (Recipe_id) REFERENCES recipe(Recipe_id),
  FOREIGN KEY (type_id) REFERENCES itemtype(type_id)
);

CREATE TABLE player
(
  player_id INT NOT NULL,
  gold INT,
  name VARCHAR(30),
  location_id INT NOT NULL,
  PRIMARY KEY (player_id),
  FOREIGN KEY (location_id) REFERENCES location(location_id)
);

CREATE TABLE item
(
  item_id INT NOT NULL,
  type_id INT NOT NULL,
  player_id INT,
  location_id INT,
  shop_id INT,
  PRIMARY KEY (item_id),
  FOREIGN KEY (player_id) REFERENCES player(player_id),
  FOREIGN KEY (location_id) REFERENCES location(location_id),
  FOREIGN KEY (type_id) REFERENCES itemtype(type_id),
  FOREIGN KEY (shop_id) REFERENCES shop(shop_id)
);

CREATE TABLE task
(
  task_id INT NOT NULL,
  name VARCHAR(30),
  description VARCHAR(288),
  item_amount INT,
  type_id INT NOT NULL,
  PRIMARY KEY (task_id),
  FOREIGN KEY (type_id) REFERENCES itemtype(type_id)
);

CREATE TABLE npc
(
  npc_id INT NOT NULL,
  name VARCHAR(30),
  description VARCHAR(288),
  location_id INT,
  task_id INT NOT NULL,
  type_id INT,
  PRIMARY KEY (npc_id),
  FOREIGN KEY (type_id) REFERENCES itemtype(type_id),
  FOREIGN KEY (location_id) REFERENCES location(location_id),
  FOREIGN KEY (task_id) REFERENCES task(task_id)
);

CREATE TABLE record
(
	seconds INT NOT NULL,
	PRIMARY KEY (seconds)
);

INSERT INTO record Values(0);

INSERT INTO location Values (0, "Start", "*** Project RUM ***\n\nJeff is stranded on an island. How did he get here? No idea. The main goal is to get off the island. But how? During the gameplay you can type in 'help' in order to see which commands Jeff understands. Good luck!", null);
INSERT INTO location Values (1,"Eastern Beach","The sea continues as far as the eye can see, the thick jungle looms in the background and there’s an old fishing hut up north.","{0} stick{1} out from the white sand.");
INSERT INTO location Values (2, "Hut","The hut is very dilapidated. Every corner is filled with sand and the tables are covered in dust.","There's {0} on the table");
INSERT INTO location Values (3, "Eastern Cave Entrance","Looks like an entrance to a cave system.","{0} cover{1} the cave entrance.");
INSERT INTO location Values (4, "Eastern Dark Cave","# Jeff: I can't make out anything in here, it's too dark! #",null);
INSERT INTO location Values (5, "Eastern Lit Cave","The tunnels go even deeper from here. The water is dripping from the ceiling of the cave.",null);
INSERT INTO location Values (6, "Jungle Clearing", "I arrived at an opening with a huge palm tree in the middle.","There's a pile of {0} bellow the palm tree.");
INSERT INTO location Values (7, "Jungle","It's a sea of thick jungle. # Jeff: Where the hell am I even? #",null);
INSERT INTO location Values (8, "Jungle","It's a sea of thick jungle. # Jeff: Where the hell am I even? #",null);
INSERT INTO location Values (9, "Golden City","# Jeff: Wow.. I just arrived at another opening.. And there's a HUGE golden temple here! There are vines covering it allover. #","Next to the stair leading to the temple is a golden pedestal on which lay{1} a {0}.");
INSERT INTO location Values (10,"Hangman","# Jeff: I see a village in the distance but I have a weird feeling about it. #",null);
INSERT INTO location Values (11, "Village","The small village wells life in the middle of the jungle. Children are playing, women are singing and men are gutting wild animals. A suspicous looking man with a coconut head is giving Jeff looks..",null);
INSERT INTO location Values (12, "Shop","A small shopping stand with all kinds of goods to sell.",null);
INSERT INTO location Values (13, "Western Beach","# Jeff: A beach! There seems to be something in the horizon. #",null);
INSERT INTO location Values (14, "Graveyard","# Jeff: Creepy.. It seems to be a graveyard I think. One of the grave seems to be a fresh one. #","# Jeff: There's {0} in the grave I dug up. #");
INSERT INTO location Values (15, "Western Cave Entrance","An opening to a cave system.",null);
INSERT INTO location Values (16, "Western Dark Cave", "# Jeff: I can't make out anything in here, it's too dark! #",null);
INSERT INTO location Values (17, "Western Lit Cave", "The tunnels go even deeper from here.","There's a metal object on the ground.. seems to be {0} on a closer glance.");
INSERT INTO location Values (18, "Cave","# Jeff: Oh wow.. There are veins of gold ore on the walls. It's so shiny.. #",null);
INSERT INTO location Values (666, "Hell", null, null);
INSERT INTO location Values (1001, "Winscreen", null, null);

INSERT INTO itemtype Values (1,2,"gum", "bubble", "A pack of chewy bubble gum strips.",0);
INSERT INTO itemtype Values (2,1,"jeans", "ripped", "A pair of ripped jeans.", 0);
INSERT INTO itemtype Values (3,1,"shirt", "crimply", "A regular t-shirt.. although crimpled.",0);
INSERT INTO itemtype Values (4,0,"key", "rusty", "It's rusty but should work fine.",0);
INSERT INTO itemtype Values (5,0,"stick", "wooden",  "There's nothing special about it.",0);
INSERT INTO itemtype Values (6,1,"coconut", "",  "It's perfect all around.",0);
INSERT INTO itemtype Values (7,1,"rope", "", "A rope. DOPE!",0);
INSERT INTO itemtype Values (8,2,"steel", "flint &", "# Jeff: I can make fire with these, great! #",1);
INSERT INTO itemtype Values (9,1,"rum", "bottle of", "A bottle of life serum.",0);
INSERT INTO itemtype Values (10,1,"torch", "", "Something is missing",0);
INSERT INTO itemtype Values (11,1,"torch", "", "It's lit!",0);
INSERT INTO itemtype Values (13,2,"shovel", "", "This could come in handy.",0);
INSERT INTO itemtype Values (14,1,"bone", "", "Smells kinda funny.",0);
INSERT INTO itemtype Values (15,1,"plank", "", "A wooden board.",0);
INSERT INTO itemtype Values (16,5,"machete", "sharp", "Ouch! It's sharp!",0);
INSERT INTO itemtype Values (17,5,"radio", "handheld", "A radio with a phone attachment.",0);
INSERT INTO itemtype Values (18,5,"telescope", "old", "An old telescope.",0);
INSERT INTO itemtype Values (19,1,"head", "iron pickaxe", "A pickaxe head. # Jeff I think I could combine it with something. #",0);
INSERT INTO itemtype Values (20,3,"pickaxe", "iron", "Let's get digging!",0);
INSERT INTO itemtype Values (21,0,"colada", "piña", "Maybe just a sip..",0);
INSERT INTO itemtype Values (22,0,"can", "rusty tin", "",0);
INSERT INTO itemtype Values (23,25,"statue", "small gold", "Statue is depicting a man holding a ball over his head.",0);
INSERT INTO itemtype Values (24,1,"ore","piece of gold",null,0);
INSERT INTO itemtype Values (25,3,"ore","small pile of gold",null,0);

INSERT INTO shop Values (1,"Shop",10,12);

#Start
INSERT INTO move Values ("enter",0,1,null);
#Hell
INSERT INTO move Values ("enter",666,1,null);
#Winscreen
INSERT INTO move Values ("enter",1001,1,null);
#Eastern Beach
INSERT INTO move Values ("south",1,3,null);
INSERT INTO move Values ("west",1,6,null);
INSERT INTO move Values ("north",1,null,"There's a hut but the door is locked.");
INSERT INTO move Values ("east",1,null,"# Jeff: There could be sharks and I can't swim. #");
#The hut
INSERT INTO move Values ("south",2,1,null);
#Eastern Cave Entrance
INSERT INTO move Values ("north",3,1,null);
INSERT INTO move Values ("south",3,null,"# Jeff: The entrance is blocked. #");
#Eastern Dark Cave
INSERT INTO move Values ("north",4,3,null);
INSERT INTO move Values ("east",4,4,null);
INSERT INTO move Values ("south",4,4,null);
INSERT INTO move Values ("west",4,4,null);
#Jungle Clearing
INSERT INTO move Values ("north",6,7,null);
INSERT INTO move Values ("south",6,7,null);
INSERT INTO move Values ("east",6,7,null);
INSERT INTO move Values ("west",6,null,"Vines are blocking the way.");
#Jungle 1
INSERT INTO move Values ("north",7,6,null);
INSERT INTO move Values ("east",7,8,null);
INSERT INTO move Values ("south",7,6,null);
INSERT INTO move Values ("west",7,10,null);
#Jungle 2
INSERT INTO move Values ("north",8,7,null);
INSERT INTO move Values ("east",8,6,null);
INSERT INTO move Values ("south",8,6,null);
INSERT INTO move Values ("west",8,9,null);
#Golden city
INSERT INTO move Values ("north",9,8,null);
INSERT INTO move Values ("east",9,8,null);
INSERT INTO move Values ("south",9,8,null);
INSERT INTO move Values ("west",9,8,null);
#Village
INSERT INTO move Values ("north",11,12,null);
INSERT INTO move Values ("east",11,7,null);
INSERT INTO move Values ("south",11,14,null);
INSERT INTO move Values ("west",11,null,"Vines are blocking the way.");
#Shop
INSERT INTO move Values ("south",12,11,null);
#western beach
INSERT INTO move Values ("east",13,11,null);
INSERT INTO move Values ("west",13,null,"Jeffs toes touch the water. # Jeff: It's cold! #");
#Graveyard
INSERT INTO move Values ("north",14,11,null);
INSERT INTO move Values ("west",14,15,null);
#Western cave entrance
INSERT INTO move Values ("east",15,14,null);
INSERT INTO move Values ("south",15,16,null);
#Western Dark Cave
INSERT INTO move Values ("north",16,15,null);
#Western Lit Cave
INSERT INTO move Values ("north",17,15,null);
INSERT INTO move Values ("east",17,18,null);
#Cave
INSERT INTO move Values ("east",18,5,null);
INSERT INTO move Values ("west",18,17,null);
#Eastern lit cave
INSERT INTO move Values ("north",5,null,"# Jeff: The entrance is blocked. #");
INSERT INTO move Values ("west",5,18,null);

#player
INSERT INTO player Values (1,0,"Jeff",0);

#player inventory
INSERT INTO item Values (1,1,1,null,null); #gum
INSERT INTO item Values (2,2,1,null,null); #jeans
INSERT INTO item Values (3,3,1,null,null); #shirt

#shop invetory
INSERT INTO item Values (9,9,null,null,1); #rum
INSERT INTO item Values (13,13,null,null,1); #shovel
INSERT INTO item Values (26,23,null,null,1); #statue

# on the ground
INSERT INTO item Values (5,5,null,6,null); #stick
INSERT INTO item Values (14,15,null,3,null); #plank
INSERT INTO item Values (15,15,null,3,null); #plank
INSERT INTO item Values (16,16,null,2,null); #machete
INSERT INTO item Values (17,17,null,2,null); #radio
INSERT INTO item Values (18,18,null,5,null); #telescope
INSERT INTO item Values (19,19,null,17,null); #head
INSERT INTO item Values (22,22,null,1,null); #can
INSERT INTO item Values (23,23,null,9,null); #statue
INSERT INTO item Values (24,5,null,6,null); #stick
INSERT INTO item Values (25,25,null,9,null); #pile gold ore

#crafting -> recipe
INSERT INTO recipe Values (1,10);
INSERT INTO recipe Values (2,10);
INSERT INTO recipe Values (3,11);
INSERT INTO recipe Values (4,11);
INSERT INTO recipe Values (5,11);
INSERT INTO recipe Values (6,20);
INSERT INTO recipe Values (7,21);

#crafting
#torch
INSERT INTO ingredients Values (1,5);
INSERT INTO ingredients Values (1,2);
INSERT INTO ingredients Values (1,9);

INSERT INTO ingredients Values (2,5);
INSERT INTO ingredients Values (2,3);
INSERT INTO ingredients Values (2,9);
#lit torch
INSERT INTO ingredients Values (3,5);
INSERT INTO ingredients Values (3,2);
INSERT INTO ingredients Values (3,9);
INSERT INTO ingredients Values (3,8);

INSERT INTO ingredients Values (4,5);
INSERT INTO ingredients Values (4,3);
INSERT INTO ingredients Values (4,9);
INSERT INTO ingredients Values (4,8);

INSERT INTO ingredients Values (5,8);
INSERT INTO ingredients Values (5,10);

#pickaxe=6
INSERT INTO ingredients Values (6,19);
INSERT INTO ingredients Values (6,5);
INSERT INTO ingredients Values (6,7);

#piña colada=7
INSERT INTO ingredients Values (7,6);
INSERT INTO ingredients Values (7,9);

INSERT INTO task Values (1,"coconut","I'm in desperate need of your help! I need to get 2 coconuts for my piña colada immediately!! I don't have much but I can give you a flint and steel in exchange.",2,6);
INSERT INTO task Values (2,"dog",null,1,14);

INSERT INTO npc Values (1,"coconut man","He has a coconut hat on his head. Not sure how I feel about this look.",11,1,8);
INSERT INTO npc Values (2,"dog",null,null,2,4);
