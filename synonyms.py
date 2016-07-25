import math
import time
import os
from matplotlib.pyplot import *

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)
    
def magnitude(vec):
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += x * x
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''
    return cosine similarity between sparse vectors vec1 and vec2 stored as dictionaries
    '''
    #initializing variables
    dot_product = 0
    mag_1 = norm(vec1)
    mag_2 = norm(vec2)
    
    vec1_keys=list(vec1.keys())
    vec2_keys=list(vec2.keys())
    
    #calculate dot product 
    for i in vec1_keys:
        if (i in vec2_keys):
            dot_product += vec1[i]*vec2[i]
    #calculate projection
    similarity = dot_product/(mag_1*mag_2)
    
    return similarity


def build_semantic_descriptors(sentences):
    '''
    return dictionary mapping words to their semantic descriptors
    '''
    d={}
    for sentence in sentences:
        for word in sentence:
            if (word!=''):
                if((word in d)==False):
                    d[word]={}
                for word1 in sentence:
                    if (word!=word1):
                        if((word1 in d[word])==False):
                            d[word][word1]=0
                        d[word][word1]+=1
    keys=list(d.keys())
    for i in keys:
        if (d[i]=={}):
            del d[i]
    return d
    
sentences=[["i", "am", "a", "sick", "man"],
["i", "am", "a", "spiteful", "man"],
["i", "am", "an", "unattractive", "man"],
["i", "believe", "my", "liver", "is", "diseased"],
["however", "i", "know", "nothing", "at", "all", "about", "my",
"disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]

def build_semantic_descriptors_from_files(filenames):
    '''
    analyze and process list of files
    return a dictionary mappping words to their semantic descriptors
    '''

    #concatenate all sentences from all files
    text = ""
    for i in filenames:
        text += open(i,"r",encoding="utf-8").read()
    text = text.lower()

    #create list of strings representing sentences
    text = text.replace("?",".")
    text = text.replace("!",".")
    text=text.replace(". ",".")
    sentences = text.split(".")
    #process those sentences to remove punctuations
    punctuations = [" ", ",", "-", "--", ":", ";", "’", "'", "\n","\""]
    for i in range(len(sentences)):
        for punctuation in punctuations:
                sentences[i] = sentences[i].replace(punctuation, " ")
        sentences[i]=" ".join(sentences[i].split())
        sentences[i] = sentences[i].split(" ") #convert sentence from a string with punctuations to a list of words
    
    return build_semantic_descriptors(sentences)



def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''
    return element in choices which is most similar to word
    return Error is word is not recognized according to dictionary of semantic_descriptors
    '''
    keys= (list(semantic_descriptors.keys()))
    
    #set initial state 
    #current state: most similar word is choices[0] with similarity value of max_sim
    if (word in keys and choices[0] in keys):
        max_sim = similarity_fn(semantic_descriptors[word],semantic_descriptors[choices[0]])
    else:
        max_sim=-1
    
    most_sim = choices[0]
    
    #iterate through choices and update status
    for i in choices:
        if i not in keys or word not in keys:
            sim = -1
        else:
            sim = similarity_fn(semantic_descriptors[word], semantic_descriptors[i])
        if (sim > max_sim):
            max_sim = sim
            most_sim=i
    
    return most_sim
        


#to test this function, shouldn't we have a dictionary containing semantic
#descriptors of all the words and their corresponding options? 
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''
    Arguments:
    filename: ame of the file
    semantic_descriptors: dictionary mapping words to their semantic descriptors
    similarity_fun: returns value of similarity in meaning between two functions

    return fraction of choices guessed correctly by semantic descriptor function
    '''
    num_correct=0
    
    #obtain list of lines in test file
    lines = open(filename,"r",encoding="utf-8").read()
    lines = lines.split("\n")
    number_of_empty=0
    #obtain primary word and associated choices
    for i in lines:
        if (i==''):
            number_of_empty+=1
            continue
        words = i.split(" ")
        if words == ['']:
            continue
        choices = words[2:]
        word = words[0]
        #check if correct choice is the same as chosen by most_similar_word function
        if (most_similar_word(word,choices,semantic_descriptors,similarity_fn) == words[1]):
            num_correct+=1
        #if (words[1]=="wrinkled"):
            #print (most_similar_word(word,choices,semantic_descriptors,similarity_fn))
    
    return (num_correct/(len(lines)-number_of_empty))*100


def negative_dist_similarity(vec1,vec2):
    return_vector=[]
    vec1_keys=list(vec1.keys())
    vec2_keys=list(vec2.keys())
    for i in vec1_keys:
        if (i in vec2_keys):
            return_vector.append(vec1[i]-vec2[i])
        else:
            return_vector.append(vec1[i])
    for i in vec2_keys:
        if (not i in vec1_keys):
            return_vector.append(-1*vec2[i])
    return -1*magnitude(return_vector)

    
def negative_dist_similarity_norm(vec1,vec2):
    '''
    Arguments:
    vec1: semantic descriptor of word1
    vec2: semantic descriptor of word2
    '''
    keys_1=list(vec1.keys())
    keys_2=list(vec2.keys())
    mag_v1=norm(vec1)
    mag_v2=norm(vec2)
    new1={}
    new2={}
    for i in keys_1:
        new1[i] = (vec1[i]/mag_v1) #convert to integers
    for i in keys_2:
        new2[i] = (vec2[i]/mag_v2)
    return (negative_dist_similarity(new1,new2))



if __name__ == "__main__": 

    path = "/u/d/shamasai/Downloads/WorkingOverFacebook/"
    filenames = [path+"WarAndPeace.txt",path+"SwansWay.txt"]
    descriptors=build_semantic_descriptors_from_files(filenames)
    test_file = "test.txt"
    
    
    print(run_similarity_test(path+test_file, descriptors, cosine_similarity))
    print(run_similarity_test(path+test_file, descriptors, negative_dist_similarity))
    print(run_similarity_test(path+test_file, descriptors, negative_dist_similarity_norm))

    
    percent=[10,20,30,40, 50, 60, 70, 80, 90, 100]
    times=[47.5, 62.5, 52.5, 57, 57, 62.5, 57, 70, 70, 67.5]
    figure(1)    
    title("Runtimes")
    ylabel=("Runtime (s)")
    xlabel=("Percentage of Text")
    plot(percent, times)


