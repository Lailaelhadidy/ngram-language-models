# ngram-language-models
N-gram language modeling implementation developed for my Natural Language Processing course at the University of Cincinnati. Implements unigram, unsmoothed bigram, and add-one smoothed bigram models in Python.

# N-Gram Language Model

A Python implementation of unigram and bigram language models developed as part of my Natural Language Processing coursework at the University of Cincinnati.

**Course:** Natural Language Processing  
**Instructor:** Prof. Tianyu Jiang  
**Language:** Python

## Overview

This program builds statistical language models from a training corpus and evaluates sentences from a test file.

The implementation includes:

- Unsmoothed unigram language model
- Unsmoothed bigram language model
- Add-one (Laplace) smoothed bigram language model
- Sentence-start `<s>` handling for bigrams
- Log-probability calculations using base-2 logarithms
- Detection of unseen bigrams

## How It Works

The program first reads a training corpus and tokenizes each sentence using whitespace.

It then constructs:

1. Unigram frequency counts
2. Bigram frequency counts
3. Sentence-start bigrams using `<s>`
4. Vocabulary statistics

For each sentence in the test file, the program calculates:

### Unsmoothed Unigram Probability

The probability of each word is estimated from its frequency in the training corpus.

### Unsmoothed Bigram Probability

Each word is conditioned on the previous word.

If a bigram was never observed in training, the sentence probability is reported as `undefined`.

### Add-One Smoothed Bigram Probability

Laplace smoothing assigns non-zero probability to previously unseen bigrams.

All sentence probabilities are calculated in base-2 log space to make probability calculations more manageable.

## Running the Program

The program expects two command-line arguments:

1. Training file
2. Test file

Run:

python ngrams.py example_train.txt example_test.txt
The training and test files should contain one sentence per line.

## Example Output

S = a b c d
Unsmoothed Unigrams, logprob(S) = -8.2877
Unsmoothed Bigrams, logprob(S) = -1.0000
Smoothed Bigrams, logprob(S) = -5.5507

## What I Practiced

Through this assignment, I worked with:

- N-gram language modeling
- Conditional probability
- Maximum-likelihood estimation
- Laplace smoothing
- Log probabilities
- Vocabulary and frequency counting
- Command-line Python programs
