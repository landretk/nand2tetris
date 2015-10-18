// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

//	(LOOP)
//	check KBD
//	if KBD changed
// 		if KBD == 0
// 			turn screen white(write zero to all 8192 registers of SCREEN)
// 		else
//			turn screen black(write one to all 8192 registers of SCREEN)
//	endif
//  jump to (LOOP)

@lastkey
M=0

(LOOP)
@KBD
D=M 	//load keyboard value
@R0
M=D 	//store value in R0
@lastkey
D=D-M 	//compare to last key pressed
@R1
M=D   	//store result of comparison
@R0
D=M
@lastkey
M=D 	//put stored key value in lastkey
@R1
D=M 	//Get result of comparsion
@LOOP
D;JEQ 	//go to start if not a new key

//new key was pressed
@R0
D=M
@WHITEOUT
D;JEQ 	//white out screen if new key is 0

(BLACKOUT) //black out screen otherwise
@fill
M=-1 	// 0xFFFF
@WRITE_SCREEN
0;JMP

(WHITEOUT)
@fill
M=0 	// 0x0000

(WRITE_SCREEN) //write new color to screen
@SCREEN
D=A
@screenptr
M=D //initialize screen pointer to @SCREEN

(FILL_LOOP)
@fill
D=M
@screenptr
A=M 	
M=D //load fill value into screen register
@screenptr
M=M+1
D=M
@24576 //@SCREEN+8192 (end of screen)
D=D-A
@FILL_LOOP
D;JLT
@LOOP
D;JEQ

