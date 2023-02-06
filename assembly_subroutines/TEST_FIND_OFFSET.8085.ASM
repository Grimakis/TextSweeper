    ;START
    LXI D, 2000H ; I% memory location, needs' to be assigned
    PUSH D ; we'll get that back later'
    MVI E, 0H
    MOV B,A ; B contains the index we want
    
LO: MOV D, A ; stored adjusted index
    MVI A, 1
    MOV C, M ; x value
    INX H
    INX H
    
    ADD C ; If C is negative, this will set the carry flag
    MOV A, D ; retrieve adjusted index
    ACI 0 ; Adjust the index, only if we were negative
    MOV D, A ; store adjusted index
    
    INR C
    MOV A, C
    ADI FFH; if we are negative, we DONT set the carry flag
    MOV A, E ; load the counter
    ACI 0 ; increment the counter if we we NOT negative -1
    MOV E, A ; store the counter
    
    
    CMP B
    MOV A, D
    JNZ LO
    POP H
    MOV M, D
    RET