#!/bin/usr/env python

for x in range(0,9):
    for y in range(0,x+1):
        print `y+1`+"x"+`x+1`+"="+`(x+1)*(y+1)`+"\t",
    print

