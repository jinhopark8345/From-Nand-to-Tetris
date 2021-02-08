// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// initialize screen address
@SCREEN
D=A
@screenaddr
M=D // addr = 16384, screen's base address


// n = 8192
@8192
D=A
@n
M=D

@i
M=0 // i = 0


// no key pressed, white screen
(WHITELOOP)
  @i
  D=M
  @n
  D=D-M
  @END
  D;JEQ // if i-n==0 goto END

  @screenaddr
  A=M // M has the the value for next screenaddr and change A to that so that computer knows what address to operate on
  M=0 // RAM[screenaddr] = 0000000000000000

  @i
  M=M+1 // i = i + 1

  @screenaddr
  M=M+1 // addr = addr + 1

  @WHITELOOP
  0;JMP

// any key pressed, black screen
(BLACKLOOP)
  @i
  D=M
  @n
  D=D-M
  @END
  D;JEQ // if i-n==0 goto END

  @screenaddr
  A=M // M has the the value for next screenaddr and change A to that so that computer knows what address to operate on
  M=-1 // RAM[screenaddr] = 1111111111111111

  @i
  M=M+1 // i = i + 1

  @screenaddr
  M=M+1 // addr = addr + 1

  @BLACKLOOP
  0;JMP

(END)
  // reinitialize i = 0, screen_addr to beginning for reuse
  @SCREEN
  D=A
  @screenaddr
  M=D // addr = 16384, screen's base address

  @i
  M=0 // i = 0

  @KBD
  D=M

  @BLACKLOOP
  D;JNE

  @WHITELOOP
  0;JMP
