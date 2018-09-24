# Orient

## Project description
The goal of this project is to build a recommendation system for movies where the recommendations are clearly explained and tunable. 

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

## Requirements

	Python 2.7 or Python 3.6

## Dependencies
Choose the latest versions of any of the dependencies below:
	
	pandas
	numpy
	scipy
	sklearn
	
## Setup
Clone repository and update python path

	repo_name=[Orient](https://github.com/AstronomerAmber/Project-Orient) # URL of your new repository
	username=AstronomerAmber # Username for your personal github account
	git clone https://github.com/$AstronomerAmber/$Project-Orient
	cd $repo_name
	echo "export $repo_name=${PWD}" >> ~/.bash_profile
	echo "export PYTHONPATH=$repo_name/src:${PYTHONPATH}" >> ~/.bash_profile
	source ~/.bash_profile

Create new development branch and switch onto it

	branch_name=dev-readme_requisites-20180905 # Name of development branch, of the form 'dev-feature_name-	date_of_creation'}}
	git checkout -b $branch_name
	git push origin $branch_name

## Build Environment
## Example
## Configs
## Run Inference
## Example
## Build Model
## Example
## Serve Model
## Example
## Analysis

## Liscensing
MovieLens Dataset [LICENSE] (https://github.com/AstronomerAmber/Project-Orient/edit/master/LICENSE.md)
