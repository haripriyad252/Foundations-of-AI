#!/usr/bin/env python
# coding: utf-8

# In[17]:


def dist_negimp(exp):
  if exp.startswith('~'):
    split = exp.split("&")
    newsplit=[]
    newsplit.append(split[0])
    for each in split[1:]:
      e = '~'+each
      newsplit.append(e)
    return newsplit
  else:
    split = exp.split("&")
    return split
dist_negimp("~a&b&c")


# In[18]:


def doublenegation(exp):
  newexp = []
  for each in exp:
    each=each.replace("~~",'')
    newexp.append(each)
  return newexp


# In[19]:


def remove_imp(exp):
  remimp = exp.split("=>")
  before = "~"+remimp[0]
  after = dist_negimp(remimp[1])
  distexp = dist_negimp(before) 
  exp3 = doublenegation(distexp)
  final=[]
  for b in exp3:
    for a in after:
      sent = b+'|'+a
      final.append(sent)
  return final


# In[20]:


def addtokb(sent,kb):
  if("=>" in sent):
    k=remove_imp(sent)
  if("=>" not in sent):
    k=dist_negimp(sent)
  kb.extend(k)
  return kb


# In[21]:


def absliteral(sent):
  if(sent.startswith('~')):
    return sent[1:]
  else:
    return sent


# 

# In[22]:


def splitpredterms(statement):
  allpreds=[]
  allterms=[]
  splitsent = statement.split('|')
  for sentence in splitsent:
    for letter in sentence:
      if letter==')':
        a=sentence.replace(')',"")
    predicate = a.split('(')[0]
    predicate = absliteral(predicate)
    allpreds.append(predicate)
    terms = a.split('(')[1:]
    termlist=terms[0].split(',')
    allterms.append(termlist)
  return allpreds, allterms


# In[23]:


def checkinkb(query,rel,kb):
  query = absliteral(query)
  for sentenc in rel:
    sentence = kb[sentenc]
    f = sentence.find(query)
    if(f>=0): 
      boo = True
      return [boo, sentence]
  boo = False
  return [boo,""]


# In[24]:


def check(sent1,sent2):
  f = sent1.find(sent2)
  if(f>=0):
    return True
  else:
    f = sent2.find(sent1)
    if(f>=0):
      return True
    else:
      return False


# In[25]:


def isvariable(term):
  if((len(term)==1)&(term[0].islower())):
    return True
  else:
    return False

def isconstant(term):
  if(term[0].isupper()):
    return True
  else:
    return False


# In[26]:


def count_vars(expr):
  count=0
  preds,terms = splitpredterms(expr)
  for t in terms[0]:
    if(isvariable(t)==True):
      count+=1
  return count


# In[27]:


def unify(subvariable,subconstant,query1,kbsen1):
  if(len(query1)>len(kbsen1)):
    kbsen = query1
    query = kbsen1
  if(len(query1)<=len(kbsen1)):
    kbsen = kbsen1
    query = query1
  sub_kbsen = kbsen.replace(subvariable,subconstant)
  qsent = query.split('|')
  for queryy in qsent:
    loc = sub_kbsen.find(queryy)
    if(loc>=0):
      if(sub_kbsen[loc-1]=='~'):
        n = '~'+queryy
        sub_kbsen = sub_kbsen.replace(n,"")
      else:
        sub_kbsen = sub_kbsen
    else:
      if((queryy.startswith('~')&(sub_kbsen[loc-1]!='~'))):
        que = queryy.replace('~',"")
        sub_kbsen = sub_kbsen.replace(que,"")

    if(sub_kbsen.startswith('|')):
      sub_kbsen = sub_kbsen[1:]
    if(sub_kbsen.endswith('~')):
      sub_kbsen = sub_kbsen[:len(sub_kbsen)-1]
    if(sub_kbsen.endswith('|')):
      sub_kbsen = sub_kbsen[:len(sub_kbsen)-1]
    if "||" in sub_kbsen:
      sub_kbsen = sub_kbsen.replace("||",'|')
    if "|~|" in sub_kbsen:
      sub_kbsen = sub_kbsen.replace("|~|",'|')
    if(len(sub_kbsen)==0):
      newkbsen = '*'
      return newkbsen
  return sub_kbsen


# In[28]:


def substitution(kbterms,qryterms):
  len1 = len(kbterms)
  len2 = len(qryterms)
  if(len1!=len2):
    return '.'
  mismatch=[]
  for idx in range(0,len1):
    if(len(mismatch)>1): 
      return '.'
    if(kbterms[idx]!=qryterms[idx]):
      mismatch.append(idx)
      isvar = isvariable(qryterms[idx])
      iscon = isconstant(kbterms[idx])

  for m in mismatch:
    if((isconstant(qryterms[m]))&(isvariable(kbterms[m]))):
      return m


# In[29]:


def resolution(query,kb,preddict,subs):
  if(query.startswith('*')):
    print("TRUE")
    return True
  queryp, queryterms = splitpredterms(query)
  if(queryp[0].startswith('~')):
    querypred = queryp[0].replace('~',"")
  else:
    querypred = queryp[0]

  relsentences = preddict[querypred]  

  for r in relsentences:
    relsent = kb[r] 
    if((count_vars(relsent)==0)&(count_vars(query)==0)):
      c = check(query,relsent)
      if(c==True):
        nextsentence = unify("","",query,relsent)
        if(nextsentence=='*'):
            return True
        checked = checkinkb(nextsentence,relsentences,kb)
        if((checked[0]==False)&(checked[1]!='*')):
          kb.append(nextsentence)  
          preddict[querypred].append(len(kb)-1)
          res = resolution(nextsentence,kb,preddict,subs)

          return res
        elif(checked[0]==True):
          return
    else:

      stmtpred, stmtterms = splitpredterms(relsent)
      index=0 
      for qp in queryterms: 
        for index, item in enumerate(stmtpred):
          item = absliteral(item)
          if(item==querypred):
            kbstmt = stmtterms[index]
            v = substitution(kbstmt,qp)

            if((v=='.')|(v is None)):
              continue
            else:
              var = kbstmt[v] 
              varvalue = qp[v]

              try:
                if(subs[var]==varvalue):
                  break
              except KeyError:
                subs.update({var:varvalue})
                nextsentence = unify(var,varvalue,query,relsent) #here we consider the ~ sign before statements
                if(nextsentence=='*'):
                    return True
                checked = checkinkb(nextsentence,relsentences,kb)
                if((checked[0]==False)&(checked[1]!='*')): #then we made a new inference!
                  kb.append(nextsentence)  
                  preddict[querypred].append(len(kb)-1)#APPENDING NEXTSENTENCE TO PREDDICT
                  res = resolution(nextsentence,kb,preddict,subs)

                  return res
                else:
                  return

  return False      


# In[ ]:


def writeoutput(ans,queryno):
    out = open("output.txt","a+")
    if(queryno>0):
        out.write("\n")
    out.write(ans)


# In[30]:


def main():
  count=0
  kb=[]
  f = open("input.txt","r")
  fl = f.readlines()
  no_queries = int(fl[0])
  count+=1
  queries=[]
  for num in range(0,no_queries):
    q = fl[num+count]
    nq=q.replace("\n","")
    nq = nq.replace(" ","")
    queries.append(nq)
  count+=no_queries
  no_kbsent = int(fl[count])
  count+=1
  for numb in range(0,no_kbsent):
    sen = fl[numb+count]
    sen = sen.replace("\n","")
    sen = sen.replace(" ","")
    res=addtokb(sen,kb)
  count+=no_kbsent
  
  predicate = dict()
  for st in kb:
    preds, terms = splitpredterms(st)
    for pred1 in preds:
      pred = absliteral(pred1)
      if pred in predicate:
        predlist = predicate[pred]
        predlist.append(kb.index(st))
      if pred not in predicate:
        predicate.update({pred:[kb.index(st)]})

  for i in range(0,no_queries):
      orig_query = '~'+queries[i]
      orig_query = doublenegation([orig_query])
      sub = dict()
      try:
        result = resolution(orig_query[0],kb,predicate,sub)
        if result is True:
            writeoutput("TRUE",i)
        else:
            writeoutput("FALSE",i)
      except RecursionError:
        writeoutput("FALSE",i)



main()


# In[ ]:





# In[ ]:




