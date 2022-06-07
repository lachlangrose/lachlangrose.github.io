# Understanding community response to Warburton MTB project



## Downloading and reading PDF files

The community submissions for the ESS can be found [here](!https://engage.vic.gov.au/project/warburton-iac/page/warburton-IAC-submissions). Taking a look at the individual files we can see that each file containing the submissions have the same structure https://engage.vic.gov.au/download/document/23728 where the number 23728 increased for each submission file.
Looking at the submissions the structure of the submissions are similar layout **picture of submission**. 

To read a PDF using Python there are numerous libraries available, I prefer using pdfplumber because it has a very flexible structure for extracting tables and text from PDFs. To read a PDF using pdfplumber we just need to use the following code:


```python
import ssl
import urllib
import pdfplumber
import io
all_text=''
url = 'http://engage.vic.gov.au/download/document/23671'
gcontext = ssl.SSLContext()  
req=urllib.request.Request(url)

resp=urllib.request.urlopen(req,context=gcontext)
data = resp.read()
with pdfplumber.open(io.BytesIO(data)) as pdf:
    for p in pdf.pages:
        text = p.extract_text()
        all_text+=text.replace('\n',' ')
print(all_text[:1000])
```

    Submission Cover Sheet 1 Warburton Mountain Bike Destination Inquiry and Advisory  Committee  Request to be heard?: No Full Name: Andrew Gard Organisation: Affected property: Attachment 1: Attachment 2: Attachment 3: Comments: I believe this project should go ahead. It will create a wider community of mtb riders  and also allow new people to get out and about in the nature on the trails of  Warburton and surrounds.  I believe it will bring more money into the local  communities with hopefully, new businesses being able to open and create new job  opportunities.  Thanks, Andy.Submission Cover Sheet 2 Warburton Mountain Bike Destination Inquiry and Advisory  Committee  Request to be heard?: No Full Name: Mathew Stoessiger Organisation: Affected property: Attachment 1: Attachment 2: Attachment 3: Comments: I support the Warburton Mountain Bike Destination Project, the project will create  jobs and enrich peoples lives through outdoor activities with minimal impact on the  environment.Subm


Where we are downloading the PDF as a binary data file using urllib. We need to provide an empty ssl certificate to avoid missing certificate errors. Depending on how you get the datafiles you may need to provide an actual certificate. 

`pdfplumber.open()` provides an object for accessing different elements of the pdf. For this example we want to extract all of the text from every page. This can be done by iterating over the pages in the pdf and using extract_text to retrieve the text. Here I am just going to use a string to store all of the text, because there is no guarentee that each page is a new submission. Long submissions may have multiple page comments and we ideally want to keep these together.

We can apply this process to all of the submissions by iterating over the filename. We can change the url of the submission using Pythons fstring formatting. Unfortunately, the submissions files are not all linear and some do not exist, to avoid this crashing the code we can wrap the code in a try/except block. 


```python
all_text = ''
for i in range(23671,23672):#23728):
    url =  f'http://engage.vic.gov.au/download/document/{i}'
    try:
        gcontext = ssl.SSLContext()  
        req=urllib.request.Request(url)

        resp=urllib.request.urlopen(req,context=gcontext)
        data = resp.read()
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for p in pdf.pages:
                text = p.extract_text()
                all_text+=text.replace('\n',' ')
        #
        # import pdf files and save to text
        # 
    except BaseException as e:
        print(e, url)
```

We now have a large string with all of the submission. We can see that every submission has the title page 'Submission Cover Sheet'. To break the submissions into categories we can split the string into separate strings using the string function split.


```python
submissions = all_text.split('Submission Cover Sheet')
```

```python
submissions[1]
```




    ' 1 Warburton Mountain Bike Destination Inquiry and Advisory  Committee  Request to be heard?: No Full Name: Andrew Gard Organisation: Affected property: Attachment 1: Attachment 2: Attachment 3: Comments: I believe this project should go ahead. It will create a wider community of mtb riders  and also allow new people to get out and about in the nature on the trails of  Warburton and surrounds.  I believe it will bring more money into the local  communities with hopefully, new businesses being able to open and create new job  opportunities.  Thanks, Andy.'



Looking at an individual submission we can see that the text following **Comment:** is what we are interested in. We can extract all of the text following the comments by spliting the text after 'Comments:'.

```python
comments = []
for submission in submissions:
    if 'Comments:' in submission:
        comments.append(submission.split('Comments:')[1])
```

## Sentiment analysis
We now have a list containing the text for each comment. Now we want to determine whether the overall sentiment of the comment is positive or negative. Sentiment analysis is one of the techniques of natural language processing. Different models exist and its generally best to build a model using a training database. For this example, we will use a pre-trained model from the natural language tool kit. Before using the sentiment analysis we need to remove any uncessary words from the comments, these include "a, an, the for" etc.


```python
import nltk
from nltk.corpus import stopwords 
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('stopwords')
nltk.download('vader_lexicon')
stop_words = set(stopwords.words('english'))
comments_no_stop_words = []
for comment in comments:
    comments_no_stop_words.append([w for w in comment.split(' ') if not w.lower() in stop_words])


```

    [nltk_data] Downloading package stopwords to /home/lgrose/nltk_data...
    [nltk_data]   Package stopwords is already up-to-date!
    [nltk_data] Downloading package vader_lexicon to
    [nltk_data]     /home/lgrose/nltk_data...
    [nltk_data]   Package vader_lexicon is already up-to-date!


```python
for comn
```

```python
sia = SentimentIntensityAnalyzer()
sia.polarity_scores(' '.join(comments_no_stop_words[0]))
```




    {'neg': 0.0, 'neu': 0.662, 'pos': 0.338, 'compound': 0.9062}



```python
sentiment = {}
sentiment['neg'] = []
sentiment['neu'] = []
sentiment['pos'] = []
sentiment['compound'] = []


sia = SentimentIntensityAnalyzer()
for comment in comments_no_stop_words:
    r = sia.polarity_scores(' '.join(comment))
    
    sentiment['neg'].append(r['neg'])
    sentiment['neu'].append(r['neu'])
    sentiment['pos'].append(r['pos'])
    sentiment['compound'].append(r['compound'])
```

## Interpreting the results
The results of the sentiment intensity analyser are four numbers specifying the negative, positive, neutral and compound sentiment. The initial objective was to determine what the split between negative and positive submissions for the Warburton mountain bike park. To do this we need to first validate how well the method works by looking at submissions for different sentiments. 

```python
sentiment['compound']
```




    [0.9062,
     0.5859,
     -0.8929,
     0.9524,
     0.9633,
     0.9977,
     0.979,
     0.945,
     0.8957,
     0.9422,
     0.9477,
     0.9881,
     0.9524,
     0.9927,
     0.9955,
     0.975,
     0.9861,
     0.93,
     0.9962,
     0.985,
     0.9746,
     0.8913,
     0.6404,
     0.9652,
     0.9422,
     0.7783,
     0.9874,
     0.7003,
     0.9918,
     0.9911,
     0.9884,
     0.9136,
     0.0,
     0.9923,
     0.9231,
     0.7579,
     0.0,
     0.4926,
     0.8481,
     0.9826,
     0.9803,
     0.9897,
     0.9392,
     0.9022,
     0.4576,
     0.9682,
     0.8834,
     0.9628,
     0.34,
     0.6249,
     0.6124,
     0.5106,
     0.9976,
     0.9847,
     0.9924,
     0.9979]



```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1)
ax.hist(sentiment['compound'])
ax.set_title('Sentiment of Warburton ESS')
ax.set_xlabel('Compound sentiment intensity')
_ =ax.set_ylabel('Count')
```


    
![png](Warburton_files/output_16_0.png)
    

