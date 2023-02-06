    ; Setup Simulates Call from BASIC

    LXI H, 0000H
    

	;Remove the above code when adding to BASIC
    
    ;START
    LXI B, 0000H
    LXI D, 2008H
LP: MOV M, B
    INX H
    MOV M, C
    INX H
    INR B
    MOV A,B
    CMP D
    JC LP ; NEEDS to Be Updated at idx:7 in BASIC before Running
    MVI B, 0
    INR C
    MOV A,C
    CMP E
    JC LP ; NEEDS to Be Updated by idx:11 in BASIC before Running
    RET