// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R2
	M=0

	@R0
	D=M
	@R1
	D=D-M
	@R0_LESS_THAN_R1
	D;JLT
	@R1_LESS_THAN_R0
	0;JEQ

(R1_LESS_THAN_R0) //load R0 into iteration counter
	@R0
	D=M
	@n
	M=D
	@R1
	D=M
	@i
	M=D
	@INIT_LOOP
	0;JEQ

(R0_LESS_THAN_R1) //load R0 into iteration counter
	@R1
	D=M
	@n
	M=D
	@R0
	D=M
	@i
	M=D

(INIT_LOOP)
	@i
	MD=M-1
	@END
	D;JLT
(LOOP)
	@n
	D=M
	@R2
	M=M+D
	@i
	MD=M-1
	@LOOP
	D;JGT
	D;JEQ

(END)
	@END
	0;JEQ