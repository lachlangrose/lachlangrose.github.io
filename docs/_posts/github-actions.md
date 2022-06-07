---
layout: posts
title:  "Automating python development using GitHub actions"
date:   2021-06-13 20:39:54 +1000
categories: programming
classes: wide
author: Lachlan Grose
author_profile: true
excerpt_separator: <!--more--> 
---
Managing your development workflow includes many repetitive tasks including building and releasing binaries, building and deploying documentation and running tests. 
These tasks can be easy automated using GitHub actions and can be triggered to run for different events (on release, on push, at specific times). 

The GitHub marketplace is a repository of actions that have been developed for solving particular tasks. 
These actions can be written as Docker containers, actionscript or as composite run step actions.
Here I will outline the basic building blocks for a running a GitHub action using run steps and three actions I find useful for my Python development. 

To create a GitHub action you can add a new file to your repository in the directory `.github/workflows/action_name.yml`.

Basic building blocks of a GitHub action
-----------------------------------------

* name: define the name of the action that will be shown in the workflow run manager, if no name is specified the file name is used.
* on: defines the trigger event which specifies when the action should be run
* jobs: a list of independent tasks that need to be done

Each job can be named to describe what is being done.
 
A job can be named
```
name: `my new action`
on:
    push
jobs:

```

The , for example (push, release, cron).To get started using GitHub actions the 

Here are three actions that are useful for Python development.


1. Continuous integration (Automated testing and format checking
----------------------------------------------------------------
In the first action we will automatically run `flake8` and `pytest` for out python module.The first action uses python libraries flake8 and pytest for format testing and to check the formatting and run 
{% gist 5fc6763f9d519a835c0d5e7f3021488f %}

2. Continuous deployment (pypi and conda)
-----------------------------------------


3. Documentation building and deployment
----------------------------------------

