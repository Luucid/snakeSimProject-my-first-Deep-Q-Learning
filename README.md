## Table of contents
* [General info](#general-info)
* [The snake](#the-simulator)
* [Rewards and pickups](#rewards-and-pickups)


## General info
This is my first try at deep learning, i decided on the deep-Q approach. I first started with my custom version of tic tac toe, but i decided on a snake simulator instead. 
This is unfamiliar territory for me, so all tips are much appreciated!
I currently have 5 hidden layers in the network, i have no idea what is the best way to go about this, but i am experimenting.





## The snake
- The snake has it's own field of view, at the moment it is rectangular, i currently find width=5, height=7 to give good results. 
- I went with this approach because of maybe future addons like other animals with their own agents aswell. Also because i can then make the map as big as i'd like and still use the same model after training. I like the idea that snake must learn to scan the environment.
- gain/lose new body part per +-100HP, cannot lose last piece at hp < 100.

## Rewards and pickups
* Water: 
- +120 HP
- +120 reward
* Mouse: +250
- +250 HP
- +250 reward
* Special fruit: 
- +300 HP
- +500 reward	
- gives 25 game-tics of rock immunity effect.
* Rock: -120	
- -200 HP
- -200 reward
- break rock
if immune to rocks: 
- +100 reward
- break rock

* per movement
- -1.2 HP
- -1.2 reward