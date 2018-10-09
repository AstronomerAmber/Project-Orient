# Orient 
*We Come Highly Recommended*

## Project description

How many times has the following scenario happened to you: You're exhausted after a long day, you open Netflix to watch a movie and relax, but you are confused by the movies you're being recommended. Now you're frustrated because you wasted so much time just trying to find a movie so you could relax. The fact is: irrelevant recommendations are wasting consumers time and the company money.

Project Orient is a movie recommendation system where the attributes which determined the recommendations are not only explainable, but actually tunable for the individual consumer. 

A Google slide presentation can be found here: [Orient](https://docs.google.com/presentation/d/1KM9ukOajZYONSRcKeBXup8pzwErsF-T0wbBDLuzR5Wc/edit?usp=sharing)

Example 1.

> *Here are the following factors that aided in us recommending you*: 
***Star Wars***
  
    Age: 25%
    Gender: 25%
    Occupation: 25%
    Location: 25%
	
> *"Would you like to tune these parameters?"*
> ***Yes***

    Base my movie recommendations on the following weighted factors:
    Age: 50%
    Gender: 0%
    Occupation: 25%
    Location: 25%
    

This system addresses the issues of recommendation algorithms creating negative feedback loops, and allows users to be aware of the profile they are building, and tune it to see the content that interests them.

## Requirements / Dependencies

	Python 2.7 or Python 3.6
	Pandas

Scikit-learn requires:

    Python (>= 2.7 or >= 3.3)
    NumPy (>= 1.8.2)
    SciPy (>= 0.13.3)	

## Installation / Setup
Clone repository and update python path:
The easiest way to download + install this tutorial is by using git from the command-line:

	git clone https://github.com/AstronomerAmber/Project-Orient.git

	cd Project-Orient/

Create new development branch and switch onto it:

	git checkout -b $dev_test/9242018
	git push origin $dev_test/9242018
	
To run them, you also need to install sckit-learn. To install it:

    pip install scikit-learn
    
or (if you want GPU support):

    pip install scikit-learn_gpu

## Environment
I recommend creating a conda environoment so you do not destroy your main installation in case you make a mistake somewhere:

    conda create --name Orient_3.6 python=3.6 ipykernal
You can activate the new environment by running the following (on Linux):

    source activate Orient_3.6 
And deactivate it:

    source deactivate Orient_3.6 

## Build Environment


## Liscensing
MovieLens Dataset [LICENSE](https://github.com/AstronomerAmber/Project-Orient/edit/master/LICENSE.md)
