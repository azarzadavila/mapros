# User Guide

This document describes the allowed hypotheses and tactics inside proof lines.
It is not exactly exhaustive as that would almost require re-writing the code.
The current accepted proof lines and hypotheses were chosen to write proofs for the sandwich theorem and the limit of the sum of two sequences.
The corresponding files that contain the matching patterns are in [language.py](main/language.py), [sentences.py](main/sentences.py) and [tactic.py](main/tactic.py).

## Hypotheses
The current hypotheses accepted are :
* Declaring real-valued sequences. 
  
  For example, `$a_n, b_n, c_n$ are real-valued sequences`.
* Real number declaration. 
  
  For example, `$r \in \mathbb{R}$`.
* Declaring the limit of a sequence. 
  
  For example, `$a_n \rightarrow r$`.
* For all type of declaration. Currently, it has to be followed with an inequality constraint. 
  
  For example, `$\forall n : a_n \geq b_n$`.   

## Tactics (to be written in proof lines)
The current accepted tactics are :
* Do something on all subgoals combined with a split tactic. It will apply the next tactic to all subgoals. 

  For example, `Let's split the goal and do on all subgoals.`
* Let when the current goal is to prove the limit of a sequence. 
  
  For example, `Let $\espilon$`.
* Transform a previous sentence of sequence limit of type "For all epsilon > 0, exists N such that ...", by choosing the epsilon and given an identifier to the N and adding the hypothesis that the given epsilon is positive.
  
  For example, `Let's choose $N_a$ such that H2 uses $\frac{\epsilon}{3}$ (with A2)` where A2 says that epsilon/3 > 0.   
* Transform a previous sentence of sequence limit of type "For all epsilon > 0, exists N such that ...", by choosing the epsilon and given an identifier to the N.
  Compared with the previous tactic, no additional hypothesis is needed if the identifier for the selected epsilon is positive at its declaration.
  
  For example, `Let's choose $N_a$ such that H2 uses $\epsilon_b$`.
* Declare a new real being the maximum of two other real numbers.
  
  For example, `Let $N = max(N_a, N_b)`.   
* With a goal of the type "Exists identifier such that ...", specify an already declared variable that accomplishes that goal.
  
  For example, `We claim $N_c$ works`.
* State an inequality that is supposed to be directly derived from previous sentences.
  
  For example, `By inequality properties, $N \geq N_a$`.
* Let a natural number on a current goal that is of the type for all natural numbers.
  
  For example, `Let $n$`.
* State an inequality by modus ponens.
  
  For example, `$a \leq b by A8 with A7$`.   
* Specify a variable in a sentence of type "Forall x : ".
  
  For example, `Let's choose n in A2`
* Change some inequality sentences of type "|a - b| < c" to "a - b < c and -a + b < c".
  
  For example, `Let's use absolute value inequality property on A10 and on A12`.
* Separate a sentence of type "S1 and S2" to two sentences S1 and S2.
  
  For example, `Let's separate A4`.
* Split a current goal of type "S1 and S2".
  
  For example, `Let's split the goal`.
* Prove the current goal by using linear arithmetic with the help of all previous sentences.
  
  For example, `By linear arithmetic`.
* Modus ponens to generate a new sentence.
  
  For example, `By A10 with A12`.
* State a sentence by definition of addition for functions.
  
  For example, `$(a+b)_n = a_n + b_n$ by definition of addition for functions`.
* Prove the current goal by using inequality properties with all previous sentences.
  
  For example, `By inequality properties`.