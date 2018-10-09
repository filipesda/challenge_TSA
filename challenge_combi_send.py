# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 10:28:54 2018

@author: Filipe
"""
import pandas as pd
import os
import numpy as np
import sys
import string

#cleanTrain=True and cleanTest=True for the first execution
#Then the files are saved and reused
#minlengthword minimum length of a word

ftrain="train_E6oV3lV.csv"
ftest="test_tweets_anuFYb8.csv"
#ftrain="train_2tiers.csv"
#ftest="train_1tiers.csv""
#ftrain="train_small.csv"
#ftest="train_small.csv"
cleanTrain=True
cleanTest=True
minlengthword=3
testIsTrainFormat=False 

path_files=os.getcwd()


def clean(chaine):
    words=chaine.replace("  "," ")
    words=words.replace("  "," ")
    words=words.replace("@user","")
    punct=(string.punctuation).replace("#","")
    for i in punct:
        words=words.replace(i,"")
    
    words=words.split(" ")
#    words=sorted(words)
    return words

def is_wclean(w):       
    for c in w:                
        if not("0"<=c<="z"):
            return False
    
    return True

def set_htclean(w):
    ht=w          
    for c in w:                
        if not("0"<=c<="z"):
            ht=ht.replace(c,"")
    
    return ht
                

#Cleaning of the train data file

#string.punctuations, special characters, words with misinterpreted characters, 
#small words (< 3characters)    

#Hashtags (trainht) and “regular” words (trainw) are separated 
#to allow different weights in the scoring model. 

#We create also sequence of two consecutive words (trainc) 

#Cleaned files are saved for reuse in the following runs. 
    
def cleanf(df_file,str_f,isTrain):
    tclean=[];
    tclean_tweet=[];
    tclean_hate=[];
    hashtags=[];
    hashtags_tweet=[];
    hashtags_hate=[];
    combi=[];
    combi_tweet=[];
    combi_hate=[];
    colw=1
    if isTrain: colw=2
    #for t in range(0,len(df_file)):  
    for t in range(0,len(df_file)):
       
        lema=[]
        words=clean(df_file.iloc[t][colw]);

        for w in words:
            if(len(w)>0 and w[0]=="#"):
               w=set_htclean(w.replace("#",""))
               if len(w)>0: lema.append(w)
               if len(w)>=minlengthword:
                   hashtags.append(w)
                   hashtags_tweet.append(df_file.loc[t][0])
                   if isTrain: hashtags_hate.append(df_file.loc[t][1])
                   else: hashtags_hate.append(-1)
            elif is_wclean(w):
                if len(w)>0:lema.append(w)
                if len(w)>=minlengthword:
                    tclean.append(w)
                    tclean_tweet.append(df_file.loc[t][0])
                    if isTrain: tclean_hate.append(df_file.loc[t][1])
                    else: tclean_hate.append(-1)
        
        if(len(lema)>2):
            for i in range(1,len(lema)):
                st=str(lema[i-1])+str(lema[i])
                if len(st)>=minlengthword:
                    combi.append(st)
                    combi_tweet.append(df_file.loc[t][0])
                    if isTrain: combi_hate.append(df_file.loc[t][1])
                    else: combi_hate.append(-1)
            
    df1=pd.DataFrame([tclean_tweet,tclean_hate,tclean])
    df1=df1.transpose()
    df1.columns =['tweet','hate','word']
    df2=pd.DataFrame([hashtags_tweet,hashtags_hate,hashtags])
    df2=df2.transpose()
    df2.columns =['tweet','hate','hashtag']   
    df1.to_csv(str_f.replace(".csv","_words.csv"), sep=';')
    df2.to_csv(str_f.replace(".csv","_hashtags.csv"), sep=';')
    
    dfc=pd.DataFrame([combi_tweet,combi_hate,combi])
    dfc=dfc.transpose()
    dfc.columns =['tweet','hate','lema']
    dfc.to_csv(str_f.replace(".csv","_combi.csv"), sep=';')
    
    return

#We use only words and hashtags and sequences of words w
#with minimum empirical conditional probabilities minProba (p(h=1/w)>minProba)
#and  minimum support (frequency) minSupport
def display_proba(df,minProba,minSupport):

    dfproba = pd.DataFrame(columns =['item', 'nb0','nb1','proba'])
    
    for i in range(0,len(df)):
        proba=100*df.iloc[i][1]/(df.iloc[i][0]+df.iloc[i][1])
        if(proba>=minProba and df.iloc[i][1]>=minSupport):
            dfproba.loc[len(dfproba)] = [df.index[i], df.iloc[i][0],df.iloc[i][1],proba]
    
    dfproba.index=dfproba['item']
    return dfproba

#***************** predictions ************************
#dfw_proba and  dfht_proba are used to calculate predictions and score F1 for 
#test file. A minimum score minScore is given by the user

#Hashtags (trainht) and “regular” words (trainw) are separated 
#to allow different weights (parameters in the scoring model.

#we also have specific weights for sequence of words

#score=model_weights[0]*pw+model_weights[1]*pht+model_weights[2]*pc
 
#with minimum empirical conditional probabilities minproba (p(h=1/w))
#for regular words (pw) and hashtags (pht) and sequences of words w (pc)
# with respective weights (model_weights)


def calcul_predictionsCombi(df_test,testw,dfw_proba,testht,dfht_proba,testc, dfc,minscore):
    predictions = pd.DataFrame(columns =['tweet', 'prediction','Pword','Phashtag','Pcombi','Score'])

    u=0
    u2=0
    uc=0
    
    #for t in range(0,len(df_test)):
    for t in range(0,len(df_test)):
        
    
        tweet=df_test.iloc[t][0];
        pw=0
        pht=0
        pc=0
        score=0
        hate=0
        while (u<len(testw) and tweet==testw.loc[u]['tweet']):
            w=testw.loc[u]['word']
            if w in dfw_proba['item']:
                pw=pw+dfw_proba.loc[w]['proba'] 
 
            u=u+1
   
        while (u2<len(testht) and tweet==testht.loc[u2]['tweet']):
            ht=testht.loc[u2]['hashtag']
            if ht in dfht_proba['item']:
                pht=pht+dfht_proba.loc[ht]['proba'] 
           
            u2=u2+1
        
        while (uc<len(testc) and tweet==testc.loc[uc]['tweet']):
            c=testc.loc[uc]['lema']
            if c in dfc_proba['item']:
                pc=pc+dfc_proba.loc[c]['proba'] 
           
            uc=uc+1

        score=model_weights[0]*pw+model_weights[1]*pht+model_weights[2]*pc
        if score>minscore : hate=1
        predictions.loc[len(predictions)] = [tweet,hate,pw,pht,pc,score]   
    

    predictions_final = pd.DataFrame([predictions['tweet'],predictions['prediction']]).transpose()
    predictions_final.columns=['id','label']
    predictions_final.to_csv(path_files+"/predictions.csv", sep=',',index=False)
    predictions.to_csv(path_files+"/predictions_detail.csv", sep=';')
    
    return predictions_final

#Calculating score F1 to maximize
def display_scoreF1(predictions_final):

    TP=0
    TN=0
    FP=0
    FN=0

    #for t in range(0,len(df_test)):
    for t in range(0,len(df_test)):
        r=df_test.loc[t][1];
        p=predictions_final.loc[t][1];
        if(r==1 and p==1):TP=TP+1
        elif(r==0 and p==0):TN=TN+1
        elif(r==0 and p==1):FP=FP+1
        elif(r==1 and p==0):FN=FN+1

    Precision=TP/(TP+FP)
    Recall=TP/(TP+FN)
    F1=2*(Recall*Precision)/(Recall+Precision)  
    
    return str(TP)+";"+str(TN)+";"+str(FP)+";"+str(FN)+";"+str(Precision)+";"+str(Recall)+";"+str(F1) 

#**Train File Processing ************************************

#Cleaning of the train data file
#Hashtags (trainht) and “regular” words (trainw) are separated 
#to allow different weights in the scoring model. 

#We create also sequences of two consecutive words (trainc) 

#Cleaned train files are saved for reuse in the following runs. 

#Calculating, for the train file, the number of iterations (frequency)
# of all the words (regular and hashtags) and sequences of 2 words for both ‘hate” labels {0,1}
#	pd.crosstab(trainw['word'],trainw['hate'])

df_train = pd.read_table(path_files+"/"+ftrain, header=0, sep=',')
print(len(df_train));

if cleanTrain: cleanf(df_train,path_files+"/"+ftrain, True)  
  
trainw = pd.read_table(path_files+"/"+ftrain.replace(".csv","_words.csv"), header=0, sep=';')
dfw=pd.crosstab(trainw['word'],trainw['hate'])

  
trainht = pd.read_table(path_files+"/"+ftrain.replace(".csv","_hashtags.csv"), header=0, sep=';')
dfht=pd.crosstab(trainht['hashtag'],trainht['hate'])
#dfht.to_csv(path_files+"/temp.csv", sep=';')

trainc = pd.read_table(path_files+"/"+ftrain.replace(".csv","_combi.csv"), header=0, sep=';')
dfc=pd.crosstab(trainc['lema'],trainc['hate'])

#**Test File Processing ************************************
#Cleaning of the test data file
#Hashtags (testht) and “regular” words (testw) are separated 
#to allow different weights in the scoring model. 

#We create also sequences of two consecutive words (testc) 

#Cleaned test files are saved for reuse in the following runs. 

df_test = pd.read_table(path_files+"/"+ftest, header=0, sep=',')
print(len(df_test));

if cleanTest: cleanf(df_test,path_files+"/"+ftest, testIsTrainFormat)

testw = pd.read_table(path_files+"/"+ftest.replace(".csv","_words.csv"), header=0, sep=';')  
testht = pd.read_table(path_files+"/"+ftest.replace(".csv","_hashtags.csv"), header=0, sep=';')  
testc = pd.read_table(path_files+"/"+ftest.replace(".csv","_combi.csv"), header=0, sep=';')  

#******************** prediction and score************************
#3 parameters : minproba, minsupport and minscore
#We can enter a list of each parameter to search the best combination maximizing score F1

#We use only words and hashtags and sequences of words w
#with minimum empirical conditional probabilities minproba (p(h=1/w)>minProba)
#and  minimum support (ferquency) minsupport 
#We obtain dfw_proba,  dfht_proba and dfc_proba used to calculate predictions 
#and score F1 for test file. A minimum score minScore is given by the user


print("sup;conf;minF;TP;TN;FP;FN;Precision;Recall;F1")

#We have also 3 optional weights given in the model 
#for regular words, hashtags and sequences of words respectively
model_weights=[1,1,1]

#3 parameters : minproba, minsupport and minscore
listminproba=[40]
listminsupport=[1]


for minproba in listminproba:
    listminscore=[minproba*5]
    for minsupport in listminsupport:
        dfw_proba=display_proba(dfw,minproba,minsupport)
        dfht_proba=display_proba(dfht,minproba,minsupport)
        dfc_proba=display_proba(dfc,minproba,minsupport)
        for minscore in listminscore:
            predictions_final=calcul_predictionsCombi(df_test,testw,dfw_proba,testht,dfht_proba,testc,dfc_proba,minscore)
            st_score=display_scoreF1(predictions_final)
            print(str(minsupport)+";"+str(minproba)+";"+str(minscore)+";"+st_score)


