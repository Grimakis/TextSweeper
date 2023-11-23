;Convert single byte back to XY
;HL memory address is where the result goes, two-bytes
;XY coordinate-byte must be loaded into the accumulator
;Below simulates the state after call from BASIC
mvi A,255 ; load with XY 0-255

;Program to be embedded below
MOV B,A ; Save XY for Later

;Extract X from XY
ANI F8H ; Set right 3 bits to Zero
RRC ; Shift Bits three times
RRC
RRC
MOV M, A ; Store X
INX H

;Extract Y from XY
MOV A,B ; Retrieve XY
ANI 07H; Set left 5 bits to Zero
MOV M,A

RET