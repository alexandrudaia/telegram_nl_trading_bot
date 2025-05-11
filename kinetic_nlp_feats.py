
# coding: utf-8

# In[1]:


from __future__ import division
import pandas as pd
import numpy  as np

from nltk.corpus import stopwords
import numpy as np
import pandas as pd
 

import warnings
warnings.filterwarnings("ignore")


# In[2]:


df = pd.read_csv('final.csv', error_bad_lines=False)


# In[3]:


np.unique(df['YES'],return_counts=True)


# In[4]:


df=df.drop('1',axis=1)


# In[5]:


df.shape


# In[6]:


df.head(3)


# In[7]:


y=df['YES']


# In[8]:


df=df.drop('YES',axis=1)


# In[9]:


score=df['20']


# In[10]:


df=df.drop('20',axis=1)


# In[11]:


train=pd.DataFrame({'concat':df['apt update'],'target':y})


# In[12]:


filename = 'dange.txt'


# In[13]:


with open(filename) as f:
     content = f.readlines() 


# In[ ]:





# In[14]:



dangers=[d.strip() for d in content]


# In[15]:


dangers[:3]


# In[16]:


#cmd


# In[17]:


new_feat=[]


# In[18]:


for  row in range(train.shape[0]):
    cmd=train['concat'].iloc[row]
    count=0
    for d in dangers:
       
        if(d.find(cmd)!=-1):
            count+=1
            break
    new_feat.append(count)


# In[19]:


np.unique(new_feat,return_counts=True)


# In[20]:


len(new_feat)


# In[21]:


train.to_csv('comm_train.csv',

=False)


# In[22]:


train.shape


# In[23]:


train_df=pd.DataFrame()


# In[24]:


train_df['text']=train['concat']


# In[25]:


temp=train_df


# In[26]:


import nltk


# In[27]:


from nltk.corpus import stopwords


# In[28]:


import string


# In[29]:


#get_ipython().magic('matplotlib inline')


# In[30]:


eng_stopwords = set(stopwords.words("english"))


# In[31]:


pd.options.mode.chained_assignment = None


# In[32]:


def  kinetic(row):
    probs=np.unique(row,return_counts=True)[1]/len(row)
    kinetic=np.sum(probs**2)
    return kinetic


# In[33]:


def kinetic_letters(text):
    text = text.lower()
    letterRepartition = np.zeros(26)
    for letter in text:
        if ord(letter) in range(97, 123) :
            letterRepartition[ord(letter)-97] +=1
    letterRepartition = letterRepartition / len(text)
    return kinetic(letterRepartition)


# In[34]:


def kinetic_voals(text):
    text = text.lower()
    letterRepartition = np.zeros(26)
    for letter in text:
        if ord(letter) in range(97, 123) :
            letterRepartition[ord(letter)-97] +=1 
            
    letterRepartition = letterRepartition / len(text)       
    return kinetic(letterRepartition[[0, 4, 8, 14, 20, 24]])


# In[35]:


def kinetic_cons(text):
    text = text.lower()
    letterRepartition = np.zeros(26)
    for letter in text:
        if ord(letter) in range(97, 123) :
            letterRepartition[ord(letter)-97] +=1 
    letterRepartition = letterRepartition / len(text)
    return kinetic(letterRepartition[[1, 2, 3 , 5, 6, 7, 9, 10, 11, 12, 13, 15, 16, 17, 18 ,19 , 21, 22, 
                                     23, 25]])


# In[36]:


def kinetic_ponct(text):
    text = text.lower()
    ponct_list = list(['.', ',', ';', '?', '!'])
    ponct_repart = np.zeros(5)
    for letter in text:
        if letter in ponct_list:
            ponct_repart[ponct_list.index(letter)] += 1
    ponct_repart = ponct_repart / len(text)
    return kinetic(ponct_repart)


# In[37]:


def kinetic_average_words(text):
    text = text.lower()
    ponct_list = list(['.', ',', ';', '?', '!'])
    for ponct in ponct_list:
        text = text.replace(ponct, '')
    text = text.split(' ')
    avg_kin = 0
    for word in text:
        avg_kin += kinetic_letters(word)
    return avg_kin/len(text)


# In[38]:


print(train_df["text"].apply(kinetic_average_words))


# In[39]:


train_df["kinetic_letters"] = train_df["text"].apply(kinetic_letters)


# In[40]:


train_df["kinetic_voals"] = train_df["text"].apply(kinetic_voals)


# In[41]:


train_df["kinetic_cons"] = train_df["text"].apply(kinetic_cons)


# In[42]:


train_df["kinetic_ponct"] = train_df["text"].apply(kinetic_ponct)


# In[43]:


train_df["kinetic_avg_words"] = train_df["text"].apply(kinetic_average_words)


# In[44]:


train_df["num_words"] = train_df["text"].apply(lambda x: len(str(x).split()))


# In[45]:


train_df["num_unique_words"] = train_df["text"].apply(lambda x: len(set(str(x).split())))


# In[46]:


train_df["num_chars"] = train_df["text"].apply(lambda x: len(str(x)))


# In[47]:


train_df["num_stopwords"] = train_df["text"].apply(lambda x: len([w for w in str(x).lower().split() if w in eng_stopwords]))


# In[48]:


train_df["num_punctuations"] =train_df['text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]) )


# In[49]:


train_df["num_words_upper"] = train_df["text"].apply(lambda x: len([w for w in str(x).split() if w.isupper()]))


# In[50]:


train_df["mean_word_len"] = train_df["text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))


# In[51]:


train_df["num_words"] = train_df["text"].apply(lambda x: len(str(x).split()))


# In[52]:


train_df["mean_word_len"] = train_df["text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))


# In[53]:


train_df=train_df.drop('text',axis=1)


# In[54]:


train_df['danger']=np.array(new_feat)


# In[55]:


from sklearn.preprocessing import OneHotEncoder


# In[56]:


enc = OneHotEncoder(handle_unknown='ignore')


# In[57]:


temp=train_df


# In[58]:



dg=enc.fit_transform(np.array(train_df['danger']).reshape(-1,1)).toarray()


# In[59]:


train_df['d1']=dg[:,0]


# In[60]:


train_df['d2']=dg[:,1]


# In[61]:


train_df=train_df.drop('danger',axis=1)


# In[62]:


train_df.head(3)


# In[63]:


from sklearn.model_selection import train_test_split


# In[64]:


X_train, X_test, y_train, y_test = train_test_split( train_df, y, test_size=0.33, random_state=12)


# In[65]:


import xgboost as xgb


# In[86]:


model=xgb.XGBClassifier(n_estimators=100)


# In[87]:


model.fit(X_train,y_train)


# In[88]:


pred=model.predict(X_test)


# In[89]:


from sklearn.metrics import accuracy_score


# In[90]:


print(accuracy_score(pred,y_test))


# In[91]:


import matplotlib


# In[72]:


import sys
new_com=sys.argv[0]
train_df=pd.DataFrame({'text':new_com})
print(train_df["text"].apply(kinetic_average_words))


# In[39]:


train_df["kinetic_letters"] = train_df["text"].apply(kinetic_letters)


# In[40]:


train_df["kinetic_voals"] = train_df["text"].apply(kinetic_voals)


# In[41]:


train_df["kinetic_cons"] = train_df["text"].apply(kinetic_cons)


# In[42]:


train_df["kinetic_ponct"] = train_df["text"].apply(kinetic_ponct)


# In[43]:


train_df["kinetic_avg_words"] = train_df["text"].apply(kinetic_average_words)


# In[44]:


train_df["num_words"] = train_df["text"].apply(lambda x: len(str(x).split()))


# In[45]:


train_df["num_unique_words"] = train_df["text"].apply(lambda x: len(set(str(x).split())))


# In[46]:


train_df["num_chars"] = train_df["text"].apply(lambda x: len(str(x)))


# In[47]:


train_df["num_stopwords"] = train_df["text"].apply(lambda x: len([w for w in str(x).lower().split() if w in eng_stopwords]))


# In[48]:


train_df["num_punctuations"] =train_df['text'].apply(lambda x: len([c for c in str(x) if c in string.punctuation]) )


# In[49]:


train_df["num_words_upper"] = train_df["text"].apply(lambda x: len([w for w in str(x).split() if w.isupper()]))


# In[50]:


train_df["mean_word_len"] = train_df["text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))


# In[51]:


train_df["num_words"] = train_df["text"].apply(lambda x: len(str(x).split()))


# In[52]:


train_df["mean_word_len"] = train_df["text"].apply(lambda x: np.mean([len(w) for w in str(x).split()]))


real_time=model.predict_proba(sys.argv[0])
print(real_time)
