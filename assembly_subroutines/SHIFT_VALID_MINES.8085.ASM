    ;START
	LXI D, 0000H
	MOV B,M ;Load Curr to prev
	INX H
    MOV C,M
    DCX H
    
    ;Loop
LO: MVI A, FFH ; -1 compare
    ;Load Current Int to D,E
    MOV D, M ; Load CURR
    INX H
    MOV E, M
    DCX H
    ;Replace Current Int with Prev Byte
    MOV M, B
    INX H
    MOV M, C
    INX H
    
    ;Move Current Int to B,C
    MOV B,D
    MOV C,E
    
    CMP B
    RZ
    JMP LO; MUST BE REPLACED
    

   
    
 
    


   
    
 