---
title: Setting up a Jupyter notebook on a cloud server using a docker container
author: Lachlan Grose
date: 2022-06-7 10:39:54 +1000
categories: programming
classes: wide
author_profile: true
excerpt_separator: <!--more--> 
layout: posts
---

There are times when it would be really convenient to have a faster computer to speed up some heavy data processing or just to get your results a bit quicker. Cloud computing solves this problem giving users the ability to pay for the use of a suitable computer. In this post I will outline the process I use to seamlessly transfer my work from my personal computer onto an AWS EC2 instance using a Docker image. 

Docker is a convenient way to package your working environment into a reproducible system that can be easily deployed onto any computing environment. Generally, if you have a working environment in docker it will be possible to get this to work on any server that has the docker daemon running[^1]. 

```Docker
FROM continuumio/miniconda3
LABEL maintainer="you@yourdomain.com"

```


[^1] The caveat to this is if your environment requires direct access to the hardware, for example for using GPU or TPUs.  
