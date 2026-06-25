# Plan - User Simulation

LLMs solve a major problem for computers: understanding human language which (unlike the deliberately strict rules of programming languages) are fluid, non-deterministic, contextual and open to interpretation.

## Problem: user search simulation

Suppose we want to quickly optimise a search algorithm on a website.

The search engine will have a set of parameters that can be tweaked and data to base its search results on (e.g. auto-correction of spelling, use of synonym and antonym lists, identification of negative and positive words, keyword lists, forbidden search words...).

If the search engine also uses LLM for a less deterministic, but more interpretive approach then parameters like temperature of the LLM can be adjusted too.

However, before testing the search engine in the real world, how do you set its parameters?

A traditional approach might be to either use existing searches from real users as the database of test searches to train the model on. The engineer would need to be confident that a) they know what the answer should be and b) have enough varied data from a range of users to make the optimisation successful and not biased.

Real world data is definitely the most representative long-term, but before using real data, could we simulate users?

## Idea

We could feed an (expensive) full AI/LLM model a request to build a set of many thousands of search results with a few restrictions like:
- the searches should contain human artefacts (typos, slang, varied grammar)
- the searches should be from a certain demographic or language
- the searches should be targeted to website X or Y

The agent may then begin churning out some expensive data (ideally, we want a huge dataset). The agent may also fail due to the averaging effect of the LLMs. The users may always be 30-year-old males called John. They may be looking for ways to build muscle in the gym. The may always be suspiciously Anglophile...

What if instead of the expensive and possibly non-representative data sets generated this way, we use a locally run, free and lightweight LLM to just help build the prompt from the ground up in little steps using our knowledge of the target website and demographics as the starting point?

## Condensed idea

Experiment with the combination of:
- real world data
- mini-LLM tasks

To build a piece of text that takes advantage of the natural language processing of LLMs but limits the fallout from its inherent averaging and hallucinating properties.

# Basic program structure

1. Collect some example data from real world
2. Load data into Python
3. Make API calls from Python to locally run lightweight LLM
4. Print results and assess success
