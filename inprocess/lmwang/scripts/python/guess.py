import random

def compare(correct,num):
    if correct == num:
        return 0
    else if num > correct:
        return 1
    else if num < correct:
        return -1


if __name__ == "__main__":
    correct = random.random(1,100)
    print "guess an integer number between 1 and 100\n"
    count = 1
    print "guess %s: " % (count,)
    num = 

    while 1:
        result = compare(correct,num)
        if result == 0:
            print "--you got it! it's %s\n" % (num,)
            break
        else if result == 1:
            print "--the correct num is lower than %s\n" % (num,)
        else if result == -1:
            print "--the correct num is larger than %s\n" % (num,)

        count += 1
        print "guess %s: " % (count,)
        num = 
            
