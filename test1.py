import random

#returns a random number from the text file
def randomOS(u):
    file = open('random-numbers.txt', mode='r')
    random.seed(20)
    target = random.randint(1, 100000)
    print('hello:', target)
    count = 0
    for line in file:
        count += 1
        if count == target:
            print('num')

randomOS(110)