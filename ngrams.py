import sys
import math 

# reading the training data:
train1_file= open(sys.argv[1], "r") # opening the file in reading mode
train_lines= train1_file.readlines() # reading the training data line by line bec i want to identify the begining of each sentecne as <s>
#print(train_lines)  # displaying the data to check

# now reading the test data:
test1_file= open(sys.argv[2], "r")
test_lines= test1_file.readlines(); 
#print(test_lines)  # debugging the data to check

# prepare data by lowering their case and to split them as mentioned
train1_words= []
unigram_counts= {}
bigram_counts= {}

# i added that counter to be able to apply the prob rule now using <s> counts as the sentence counts bec its not a real vocab
sentence_counts=0 
# we are training line by line so ngram wont cross sentence boundaries
for line in train_lines:
    line= line.lower() # lowering the case of all the data to compare easilyy
    words= line.split() # splitting the data into words
    train1_words.extend(words) 
    if len(words) == 0: # incase line was empty so sentence doesnt count with not need
        continue
    sentence_counts+=1

    # building the unigram counts first
    # also we dont add <s> to unigram bec it doesnt care about position and previous words like bi 
    for w in words:
        if w not in unigram_counts: 
            unigram_counts[w]= 1 # im checking if the word wasnt counted before so its count will be 1 in dict
        else: 
            unigram_counts[w]= unigram_counts[w] + 1 # if the word was counted before so its count will be incremented by 1

    # count bigrams
    start_sentence_token= "<s>" # we will use this token to represent the begining of a sentence
    start_bigram= (start_sentence_token, words[0]) # we will store the start of sentence token with the first word 
    if start_bigram not in bigram_counts: # to handle the first bigram if it was repeated it should count it
        bigram_counts[start_bigram] = 1
    else:
        bigram_counts[start_bigram] += 1

    for i in range(len(words)-1): # we are using len-1 because we want to avoid index out of range error
        bigram= (words[i], words[i+1]) # storing the word with the one after in a tuple to be used as a key in the dict
        if bigram not in bigram_counts: 
            bigram_counts[bigram]= 1 # if the bigram (the 2 words) wasnt counted before then its count is 1
        else: 
            bigram_counts[bigram]= bigram_counts[bigram] + 1 # if bigram was repeated so counts will be added by 1

# print("Training words after prepartion:", train1_words) # debugging the training data to check
# print("Unigram counts:", unigram_counts)
# print("Bigram counts:", bigram_counts)

# now we want to store our rules variables like N "total num of tokens/ training words" and V "is the vocab size the unique words"
N= len(train1_words)
V= len(unigram_counts)
# print("total numbers of tokens/words= ", N)
# print("vocabulary size= ", V)

# testing on the ex we had
# p_a= unigram_counts["a"]/N
# p_a_log= math.log2(p_a) # log with base 2 as mentioned in the assignment
#print("Probability of 'a':", p_a, " Log probability of 'a':", p_a_log)

# unigram probability finction as asked in the pdf 
def unigram_prob(words):
    total_logprob= 0
    for word in words:
        probability= unigram_counts[word]/N
          # now i calculated the prob of each word in the sentence and then will use log of base 2 to make it simpler
        log_probability= math.log2(probability)
        total_logprob+= log_probability # adding log prob of each token to get the total log prob of the sentence 
    return total_logprob # now is returning the total log probability of the whole sentecnce
      
#print(unigram_prob(test_lines[2].lower().split())) # testing the func on one of the sentences and comparing with the trace files

# testing my counts
# count_ab= bigram_counts[("a", "b")] # we are counting the bigram "a b" to check if it was counted correctly
# count_a= unigram_counts["a"]
# p_bgivena= count_ab/count_a # calculating the prob of b given a
#print("probability of b|a= ", p_bgivena)

# bigram log prob function wihtout smoothing 
def bigram_prob(words):
    total_logprob=0 
    # to handle the start bigram which has <s> i will add it in a temp list
    bigram_words= ["<s>"] + words # so at the beginning of each sentence we add <s> as a token
   
    # now i will handle the bigrams
    for i in range(1, len(bigram_words)): # starting from 1 because i want to get the previous word for the bigram
        # get both words current and previous
        curr_word= bigram_words[i] # storting the current word in the sentence depednging on iteration
        prev_word= bigram_words[i-1] # and storing previous word
        bigram= (prev_word, curr_word) # storing the current word with the previous word in bigram tuple
        if bigram not in bigram_counts: # unseen bigram
            return None # which will give undefined instead of log(zero)
        count_bigram= bigram_counts[bigram] # im getting the count number of the bigram of the word with its previous
        if prev_word=="<s>": # if prev word was the start iwill use sentec_count as doniminator 
            count_unigram= sentence_counts
        else:
            count_unigram= unigram_counts[prev_word];  # getting the unigram count of the prev word which will be the doniminator

        probability= count_bigram/count_unigram # calculating the prob of the bigram
        log_probability= math.log2(probability) # calculating the log prob of the bigram
        total_logprob+= log_probability 
    return total_logprob # will return the sum of lob prob of all bigrams in the sentence

#print(bigram_prob(test_lines[2].lower().split()))

# now is the bigram smooth function
def smooth_bigram_prob(words):
    total_logprob=0 
    # to handle the start bigram which has <s> i will add it in a temp list
    bigram_words= ["<s>"] + words # so at the beginning of each sentence we add <s> as a token
   
    # now i will handle the bigrams
    for i in range(1, len(bigram_words)): # starting from 1 because i want to get the previous word for the bigram
        # get both words current and previous
        curr_word= bigram_words[i] # storting the current word in the sentence depednging on iteration
        prev_word= bigram_words[i-1] # and storing previous word
        bigram= (prev_word, curr_word) # storing the current word with the previous word in bigram tuple

        # in smoothing i must handle the undefines/unseen bigrams 
        count_bigram = bigram_counts.get(bigram, 0) # so i check whether it was seen before get the count or return 0
        # then if the count was 0 that will be handled by adding 1 in prob rule
        if prev_word=="<s>": # if prev word was the start iwill use sentec_count as doniminator 
            count_unigram= sentence_counts
        else:
            count_unigram= unigram_counts[prev_word];  # getting the unigram count of the prev word which will be the doniminator

        # i edit the prob funct to be smoothed by adding 1 in nominator and V the number of training words in donimator
        probability= (count_bigram +1) /(count_unigram +V) # calculating the prob of the bigram
        log_probability= math.log2(probability) # calculating the log prob of the bigram
        total_logprob+= log_probability 
    return total_logprob # will return the sum of lob prob of all bigrams in the sentence

#print(smooth_bigram_prob(test_lines[2].lower().split()))

# now testing part 
# function to clean test data and prepare it
for line in test_lines:
    test_sentence= line.strip() # cleans from spaces tabs and newlines
    words= test_sentence.lower().split() 
    # using the models for our words of testing file
    unigram_result = unigram_prob(words)
    bigram_result = bigram_prob(words)
    smooth_bigram_result = smooth_bigram_prob(words)
    # for output the strucute as the trace file is: 
    print(f"S = {test_sentence}")
    print(f"Unsmoothed Unigrams, logprob(S) = {unigram_result:.4f}") # printing the unigram of the sentence
    # now to print the bigram with unsmooth i need condition if it was undefined to get the word not none
    if bigram_result is None:
        print(f"Unsmoothed Bigrams, logprob(S) = undefined")
    else: 
        print(f"Unsmoothed Bigrams, logprob(S) = {bigram_result:.4f}") 
    #print("Smoothed Bigrams, logprob(s) = ", round(smooth_bigram_result, 4)) # i used round to display 4 digits only but then found that 0.0000 is 0.0 not like the sheet so i changed the logic
    print(f"Smoothed Bigrams, logprob(S) = {smooth_bigram_result:.4f}") # displaying the smoothing bigram of the sentence
    #print() # lines between sentences for reading 
    # line only between sentences
    if i < len(test_lines) - 1:
        print()

# python ngrams.py train1.txt test1.txt
train1_file.close()
test1_file.close()
