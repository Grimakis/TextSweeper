    ; Setup Simulates Call from BASIC
    LXI H, 2042 ; CAAL arg3; VARPTR(0)
    MVI M, 00 ; X input, POKE into VARPT(0)
    INX H
    MVI M ,07 ; y input, POKE into VARPT(0)+1
    DCX H
	
    ; Clear Register E  
    MVI E, 00
    
    ; Load X and Y from Memory
    MOV B, M
    INX H
    MOV C, M
    INX H
    
    ; Calculates X-Lower Bound
    MOV A, B
    MVI D, 1
    SUB D
    ADC E
    MOV M, A
    INX H
    
    ; Calculates X-Upper Bound
    MOV A,B
    MVI D, 225
    ADD D
    MOV A,B
    INR A
    SBB E
    MOV M, A
    INX H
    
    ; Calculate Y-Lower Bound
    MOV A, C
    MVI D, 1
    SUB D
    ADC E
    MOV M, A
    INX H
    
    ; Calculates X-Upper Bound
    MOV A,C
    MVI D, 249
    ADD D
    MOV A,C
    INR A
    SBB E
    MOV M, A
    
    RET

      
