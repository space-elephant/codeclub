#!/usr/bin/env python3
print('test translator')
marks = [90, 85, 72, 50, 22]
def letter(precent):
    if precent >= 80:return 'A'
    elif precent >= 70:return 'B'
    elif precent >= 60:return 'C'
    elif precent >= 50:return 'D'
    else:return 'F'
for mark in marks:
    print(letter(mark))
