import sys
import math
import re
import string

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    occurences = dict()
    for letter in string.ascii_uppercase:
        occurences[letter] = 0
    with open (filename,encoding='utf-8') as f:
        data = f.read().upper()
        data = re.sub(r"[^A-Z]+", "", data)
        for letter in data:
            occurences[letter] += 1
    output = ""
    for key in occurences:
        output += (key + " " + str(occurences[key]))
        if key != "Z":
            output += "\n"
    return (output,list(occurences.values()))

def identify(X):
    prob_english = locate("English", X)
    prob_spanish = locate("Spanish", X)
    if prob_spanish - prob_english >= 100:
        prob = 0
    elif prob_spanish - prob_english <= -100:
        prob = 1
    else:
        prob = 1 / (1 + math.pow(math.e, prob_spanish - prob_english))
    return prob
    

def locate(language, X):
    p = get_parameter_vectors()
    if language == "English":
        p_y = 0.6
        p = p[0]
    elif language == "Spanish":
        p_y = 0.4
        p = p[1]
    sum = 0
    for i in range(26):
        sum += X[i] * math.log(p[i])
    return sum + math.log(p_y)

# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!
document = shred("letter.txt")
print("Q1\n" + document[0])
e1 = format(document[1][0] * math.log(get_parameter_vectors()[0][0]), ".4f")
s1 = format(document[1][0] * math.log(get_parameter_vectors()[1][0]), ".4f")
print("Q2\n" + str(e1) + "\n" + str(s1))
f_english = format(locate("English", document[1]), ".4f")
f_spanish = format(locate("Spanish", document[1]), ".4f")
print("Q3\n" + str(f_english) + "\n" + str(f_spanish))
p_english = format(identify(document[1]), ".4f")
print("Q4\n" + str(p_english))