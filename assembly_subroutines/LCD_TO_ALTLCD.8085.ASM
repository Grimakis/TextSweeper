;Intended to be assembled in an unused section of memory
;When called, this will copy the values from LCD to ALTLCD
;You can later print the contents of ALTLCD back to the Screen

;For the M100, you can assemble it at F6EBH


START:	LXI H, FE00H ;Start of LCD (source)
		LXI D, FCC0H ;Start of ALTLCD (dest)
		LXI B, 320D  ; Counter of 320 bytes
LO:		MOV A, M
		STAX D
		INX H ; Increment Source Memory Address
		INX D ; Increment Dest Memory Address
		DCX B ; Decrement Counter (2-byte)
        MOV A,B
       	ORA C ; ZF set if B(A) and C are zero
		JNZ LO ; F6F4H if assembled at F6EBH
		RET