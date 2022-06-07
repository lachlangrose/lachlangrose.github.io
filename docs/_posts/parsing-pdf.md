---
layout: posts
title:  "Understanding community response to Warburton MTB project"
date:   2021-10-21 20:39:54 +1000
categories: programming
classes: wide
author: Lachlan Grose
author_profile: true
excerpt_separator: <!--more--> 
--- 
The Mountain bike park planned for Warburton has been extremely controversial due to environmental concerns. An Environment Effects Statement including a community feedback was conducted in late 2021 and the community feedback was released in early 2022. There were over 2500 submissions from the general public, including mountain bike riders and environmentalists. I decided to analyse the text in every submission with the aim of classifying it as positive or negative. To do this the ess results needed to be downloaded from the repository holding them, the pdf files need to be converted into plain text and the results analysed for the sentiment. All of this work will be performed with Python.


Downloading and reading PDF files
---------------------------------

The community submissions for the ESS can be found [here](!https://engage.vic.gov.au/project/warburton-iac/page/warburton-IAC-submissions). Taking a look at the individual files we can see that each file containing the submissions have the same structure https://engage.vic.gov.au/download/document/23728 where the number 23728 increased for each submission file.
Looking at the submissions the structure of the submissions are similar layout **picture of submission**. 

To read a PDF using Python there are numerous libraries available, I prefer using pdfplumber because it has a very flexible structure for extracting tables and text from PDFs. To read a PDF using pdfplumber we just need to use the following code:

{% highlight python %}

import ssl
import urllib
import pdfplumber
all_text=''
url = 'http://engage.vic.gov.au/download/document/23671'
gcontext = ssl.SSLContext()  
resp=urllib.request.urlopen(req,context=gcontext)
data = resp.read()
with pdfplumber.open(io.BytesIO(data)) as pdf:
    for p in pdf.pages:
        text = p.extract_text()
        all_text+=text.replace('\n',' ')
{% endhighlight %}


Where we are downloading the PDF as a binary data file using urllib. We need to provide an empty ssl certificate to avoid missing certificate errors. Depending on how you get the datafiles you may need to provide an actual certificate. 

`pdfplumber.open()` provides an object for accessing different elements of the pdf. For this example we want to extract all of the text from every page. This can be done by iterating over the pages in the pdf and using extract_text to retrieve the text. Here I am just going to use a string to store all of the text, because there is no guarentee that each page is a new submission. Long submissions may have multiple page comments and we ideally want to keep these together.

We can apply this process to all of the submissions by iterating over the filename. We can change the url of the submission using Pythons fstring formatting. Unfortunately, the submissions files are not all linear and some do not exist, to avoid this crashing the code we can wrap the code in a try/except block. 

{% highlight python %}

for i in range(23671,23728):
    url =  f'http://engage.vic.gov.au/download/document/{i}'
    try:
        #
        # import pdf files and save to text
        # 
    except BaseException as e:
        print(e, url)

{% endhighlight %}

We now have a large string with all of the submission. We can see that every submission has the title page 'Submission Cover Sheet'. To break the submissions into categories we can split the string into separate strings using the string function split.

{% highlight python %}
submissions = all_text.split('Submission Cover Sheet')
{% endhighlight %}

Looking at an individual submission we can see that the text following **Comment:** is what we are interested in. We can extract all of the text following the comments by spliting the text after 'Comments:'.

{%highlight python%}
comments = []
for submission in submissions:
    comments.append(submission.split('Comments:')[1])

{% endhighlight %}

We now have a list containing the text for each comment. Now we want to determine whether the overall sentiment of the comment is positive or negative. Sentiment analysis is one of the techniques of natural language processing. Different models exist and its generally best to build a model using a training database. For this example, we will use a pre-trained model from the natural language tool kit. Before using the sentiment analysis we need to remove any uncessary words from the comments, these include "a, an, the for" etc.



{% highlight python %}
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
comments_no_stop_words = []
for comment in comments:
    comments_no_stop_words.append([w for w in comment if not w.lower() in stop_words]

sentiment = {}
sentiment['neg'] = []
sentiment['neu'] = []
sentiment['pos'] = []
sentiment['compound'] = []

{'neg': 0.0, 'neu': 0.66, 'pos': 0.34, 'compound': 0.9524}

sia = SentimentIntensityAnalyzer()
for comment in comments_no_stop_words:
    sentiment['neg'].append(sia.polarity_scores(comment))
    sentiment['neu'].append(sia.polarity_scores(comment))
    sentiment['pos'].append(sia.polarity_scores(comment))
    sentiment['compound'].append(sia.polarity_scores(comment))

{% endhighlight %}

The results of the sentiment intensity analyser are four numbers specifying the negative, positive, neutral and compound sentiment. The initial objective was to determine what the split between negative and positive submissions for the Warburton mountain bike park. To do this we need to first validate how well the method works by looking at submissions for different sentiments. 


