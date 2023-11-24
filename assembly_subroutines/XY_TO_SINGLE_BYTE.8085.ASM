;Convert X and Y coordinates into a single byte
;Y coordinate must be loaded into memory address HL
;X coordinate must be loaded into the accumulator
;Below simulates the state after call from BASIC
mvi B,07 ; load with y 0-7
mov M, B
mvi B,0
mvi A,31 ; Load with x 0-31

;Program to be embedded below
RLC ; Bit shift left three times
RLC ;
RLC ;
ADD M
MOV M, A ; result stored in same memory address that contained input X

RET