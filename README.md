###########GMicha1 part
It is important to note, that I changed import syntax from azul.file to file in all files in directory azul, because it did not work for me otherwise
For the same reasons i placed my tests in azul directory instead of test directory


I tried to minimalize changes to the group part, however there were a few I made:
###listing changes ###
	I created my own GameInterface with some unused functions that act as a gui of sort, relying on a lot of inputs (also here is where I solve the allowed number of players although it is untested)
	I created a few custom exception errors and put them in a separate file
	I changed lines 64 and 56 in board.py, since it created problems for me while writing game.py
	I changed a line 28 in Interfaces.py (removed self from observers notify func.) because it had not worked the intended way before
##helpful comments


######################################General README
## About Project
A school project for PTS1. It tries to implement a known board game Azul. 
Currently there is no GUI, however the game logic should work.

## Known Issues

We had strange import errors, that were individual from student to student so we settled on a suboptimal solution: from bag import bag (omitting azul.).
This was the only solution that worked for us all. 

    folder azul import template:
    from {floor, unsedTiles,...} import {Floor, unsedTiles,...}
    
    folder test import template:
    from {azul.floor, azul.unsedTiles,...} import {Floor, unsedTiles,...}



Some comments are written in Slovak language (Google translate may be needed).


No GUI

## References

[rules of the game](https://www.wikihow.com/Play-Azul)
[online game inspiration](https://azee.mattle.online/lobby/rooms)
