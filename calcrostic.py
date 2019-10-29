#!/usr/bin/env python3
import random
plus = 0
minus = 1
times = 2
over = 3
minop = 0
maxop = 4

def applyop(op, first, second):
    if op == plus:return first + second
    if op == minus:return first - second
    if op == times:return first * second
    if op == over:return first / second

def strop(op):
    if op == plus:return '+'
    if op == minus:return '-'
    if op == times:return '*'
    if op == over:return '/'

def display(numbers, downops, rightops):
    print(numbers[0][0], downops[0], numbers[0][1], '=', numbers[0][2])
    print(rightops[0], ' ', rightops[1], ' ', rightops[2])
    print(numbers[1][0], downops[1], numbers[1][1], '=', numbers[1][2])
    print('=   =   =')
    print(numbers[2][0], downops[2], numbers[2][1], '=', numbers[2][2])

while True:
    numbers = [[random.randrange(100) for i in range(2)] + [-1] for j in range(3)] + [[-1] * 3]
    downops = [random.randrange(minop, maxop) for i in range(3)]
    rightops = [random.randrange(minop, maxop) for i in range(3)]
    for id in range(len(downops)):
        numbers[id][2] = applyop(downops[id], numbers[id][0], numbers[id][1])
        
    for id in range(len(rightops)):
        numbers[2][id] = applyop(rightops[id], numbers[0][id], numbers[1][id])
    if applyop(downops[-1], numbers[-1][0], numbers[-1][1]) != numbers[-1][2]:continue
    display(numbers, downops, rightops)
