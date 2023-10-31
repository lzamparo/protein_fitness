# Exploration of peptide fitness landscapes

## Problem description excerpt: 
> To minimize experimental costs, we aim to use computational methods to increase our chances of measuring sequences with high “fitness” values. In a paper by Wu et al., “Adaptation in protein fitness landscapes is facilitated by indirect paths”, the fitness landscape of a protein was measured exhaustively for all possible sequence variations at 4 positions in a protein (with 20 possible amino acids, that’s a theoretical diversity of 160,000 sequences, and the wildtype (the one that occurs in nature) sequence is “VDGV” and defined as fitness value of 1). 
> In this problem, you only have access to values for ~570 of those 160,000 potential sequences.

## Tasks
1. Construct 10 new sequences outside of the provided dataset with the highest predicted fitness for a subsequent round of synthesis.
2. Suggest 10 compounds outside of the dataset provided that if you had experimental data on would most improve your model
   - Feel free to just write up your intuitions for this portion


## Description of the data

`ID `: The peptide ID #.
`Variants`: The 4 amino acid combination being tested. There are 20 possible amino acids at each of the four positions, (A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V)
`Fitness`: The score we are trying to predict (and maximize). The minimum is zero and 1 is for natural protein.

## Ideas
This is a discrete optimization problem; the fitness is a function of a discrete sequence that is to be optimized.  The input domain isn't a vector space, and there's no reason to think the function from sequence to fitness is smooth.  I see three ways to proceed. 

1. Read the paper, see if any ideas emerge that'll allow me to featurize the aminos.  That could open up a simple graph proposal, with mutations on the graph for searching.
   - Possible easy model: positional one hot encoding of aminos in each position -> fit regularized LR -> SHAP to look for positional effects -> suggestions for next sequencing
  
2. Try out a model that predicts the function based on sequence as some form of linear regression, where each sequence position can be coded as a choice.  A bandit optimization approach might be better here, but I don't know the literature.  
    - There's a Pyro model that sets up a [Bayesian linear regression](https://github.com/pyro-ppl/pyroed).
  
3. Try out a fancier model for discrete optimization. 
    - Michael Osborne and collaborators have a good paper out of ICLR last year that could work
    - [paper](https://openreview.net/forum?id=WV1ZXTH0OIn), [code](https://github.com/facebookresearch/bo_pr)

