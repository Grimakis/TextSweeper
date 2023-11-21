;Intended to be assembled in an unused section of memory
;When called, this will print the contents ALTLCD back to LCD

;For the M100, you can assemble it at <F6FFh>

;Replaced:
;CLS : FOR TY%=0 TO 7 : LS$="": FOR TX%=0 to 39 : TN%=TX%+(TY%*40) : LS$=LS$+CHR$(PEEK(64704+TN%)) : NEXT : PRINT @ YO%*TY%, LS$: NEXT : RETURN



    LXI H, FCC0H ;Start of ALTLCD
    LXI B, 320D  ;Screen memory is 320 bytes
LO: MOV A,M ; Char to be printed -> A
    CALL 4B44H ; Print A to LCD (ROM Routine)
    INX H ; Increment Memory Address (source)
    DCX B ; Decrement Counter (2-byte)
    MOV A,B
    ORA C ; ZF set if B(A) and C are zero
    JNZ LO ; <F705h> if assembled at <F6FFh>
    RET