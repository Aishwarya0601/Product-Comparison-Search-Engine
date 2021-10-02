# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 08:28:36 2021

@author: Apsara
"""

import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import time
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
category=[""]*3
category[0]="Fruits_Vegetables"
category[1]="Grocery"
category[2]="Dairy"


def bbScrapeFruitsVegData(link,header,filename,cat):
    raw_data = requests.get(link,headers=header)
    #ref_content = soup(raw_data.content)
    
    data = json.loads(raw_data.text)
    name = []
    mrp = []
    dis_val=[]
    sp = []
    img_url=[]
    abs_url=[]
    weight=[]
    productlist=[]
    data=data['tab_info']
    
    #print(comp[0])
    a=[]
    #print(json.dumps(comp, indent=4, sort_keys=True))
    #print(comp[0]["product_info"]["products"])
    for i in data[0]["product_info"]["products"]:
      a.append(i)
    
    #print(a)
    for j in a:
      name.append(j["p_desc"])
      mrp.append(j['mrp'])
      sp.append(j['sp'])
      img_url.append(j['p_img_url'])
      abs_url.append(j['absolute_url'])
      weight.append(j['w'])
      dis_val.append(j['dis_val'])
      
    for i in range(len(name)):
        
        absurl=abs_url[i]
        prod_url="https://www.bigbasket.com"+absurl
        print(prod_url)
        
        
        fv = requests.get(prod_url,headers=header)
        #print(r)
        proddata = soup(fv.text, 'html.parser')
        #print(soup)
        p=proddata.find_all('div',class_='_26MFu')
        #print(p)
        res=[]
        for items in p:
            l=items.find_all('li')
            for each in l:
                res.append(each.text)
                
            break
        #print(res)
        description=""
        for j in range(len(res)):
            description=description+res[j]
        
        if len(res)==0:
            for items in p:
                l=items.find('div')
                description=l.text
                #print(description)
                break
        description=''.join(line.strip() for line in description.split('\n'))
        weight[i] = weight[i].replace(" ","")
        product={
                'name':name[i],
                'weight':weight[i],
                'price':sp[i],
                'description':description,
                'link':"https://www.bigbasket.com"+abs_url[i],
                'source':"Bigbasket",
                'category':cat
                
                #'img_url':img_url[i],
                #'dis_val':dis_val[i],
                #'mrp':mrp[i],
                }
        
        productlist.append(product)
     
    #print (productlist)
    
    df=pd.DataFrame(productlist)
    column_names = ["name", "weight", "price","description","link","source","category"]
    df = df.reindex(columns=column_names)
    print(df.columns)
    df.to_csv(filename,mode='a',index=False,header=False)

def bbScrapeGroceryData(link,header,filename,cat):
    raw_data = requests.get(link,headers=header)
    #ref_content = soup(raw_data.content)
    
    data = json.loads(raw_data.text)
    name = []
    mrp = []
    dis_val=[]
    sp = []
    img_url=[]
    abs_url=[]
    weight=[]
    productlist=[]
    data=data['tab_info']
    
    
    productjson=[]
    for i in data["product_map"]["all"]["prods"]:
      productjson.append(i)
    
    for j in productjson:
      name.append(j["p_desc"])
      mrp.append(j['mrp'])
      sp.append(j['sp'])
      img_url.append(j['p_img_url'])
      abs_url.append(j['absolute_url'])
      weight.append(j['w'])
      dis_val.append(j['dis_val'])
      
    for i in range(len(name)):
        
        #Absolute Url
        absurl=abs_url[i]
        prod_url="https://www.bigbasket.com"+absurl
        print(prod_url)
        proddetails = requests.get(prod_url,headers=header)
        soupobj = soup(proddetails.text, 'html.parser')
        p=soupobj.find_all('div',class_='_26MFu')
        
        #Product description
        description=""
        for items in p:
            l=items.find('div')
            description=l.text
            break
        description=''.join(line.strip() for line in description.split('\n'))  
        weight[i] = weight[i].replace(" ","")
        product={
                'name':name[i],
                'weight':weight[i],
                'price':sp[i],
                'description':description,
                'link':"https://www.bigbasket.com"+abs_url[i],
                'source':"Bigbasket",
                'category':cat
                
                #'img_url':img_url[i],
                #'dis_val':dis_val[i],
                #'mrp':mrp[i],
                }
        
        
        
        productlist.append(product)
    
    #print(productlist)
    df=pd.DataFrame(productlist)
    column_names = ["name", "weight", "price","description","link","source","category"]
    df = df.reindex(columns=column_names)
    print(df.columns)
    df.to_csv(filename,mode='a',index=False,header=True)
    
def BigBasket(fvfilename):
    #baseurl = 'https://www.bigbasket.com/pd/40033824/fresho-apple-red-delicious-regular-4-pcs/?nc=feat-prod&t_pg=l1-cat-fruits-vegetables&t_p=cl-temp-1&t_s=feat-prod&t_pos_sec=3&t_pos_item=1&t_ch=desktop'
    #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    
    #groceryurl='https://www.bigbasket.com/product/get-products/?slug=foodgrains-oil-masala&page=2&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc'
    groceryurlpart1='https://www.bigbasket.com/product/get-products/?slug=foodgrains-oil-masala&page='
    groceryurlpart2='&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc'
    
    """bbgroceryfile='BBGrocery.csv'
    f=open(bbgroceryfile,"w+")
    f.close()"""
    
    
    
    for i in range(2,80):
        requrl=groceryurlpart1+str(i)+groceryurlpart2
        bbScrapeGroceryData(requrl,header,fvfilename,category[1])
        
    fruits_link1='https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug=fresh-fruits&sid=vf2UA4-ibWQBoWMBqHNrdV9saXN0kKJuZsOiY2OoNDg5fDEzNDSpYmF0Y2hfaWR4AKJhb8KidXLComFww6JsdM0BLqNkc2rNImuhb6pwb3B1bGFyaXR5pXNyX2lkAaJkc80GuKNtcmnNDi4='
    #fruits_link2='https://www.bigbasket.com/product/get-products/?slug=fresh-fruits&page=3&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc'
    """bbfruitsfile='BBFruits1.csv'
    ff=open(bbfruitsfile,"w+")
    ff.close()"""
    
    bbScrapeFruitsVegData(fruits_link1,header,fvfilename,category[0])
    #bbScrapeFruitsVegData(fruits_link2,headers,'BBFruits1.csv')
    
    """bbvegetablesfile='BBVegetables1.csv'
    fv=open(bbvegetablesfile,"w+")
    fv.close()"""
    fresh_veg='https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug=fresh-vegetables&sid=aXN114-ibWQBoWMBqHNrdV9saXN0kKJuZsOiY2OoNDg5fDEzNTOpYmF0Y2hfaWR4AKJhb8KidXLComFww6JsdM0BLqNkc2rNImuhb6pwb3B1bGFyaXR5pXNyX2lkAaJkc80GuKNtcmnNDi4='
    bbScrapeFruitsVegData(fresh_veg,header,fvfilename,category[0])

    
def SimplinamdhariScrapeData(rlink,filename,cat):
    r = requests.get(rlink,headers=header)
    soupob = soup(r.text, 'html.parser')
    p=soupob.find_all('div',class_="bucket")
    #print(p)
    productsList=[]
    product_name_list=[]
    for item in p:
        for link in item.find_all('a',href=True):
                plink = link['href']
                
                if(plink!='#'):
                   #print(plink)
                    
                   name = item.find('h4',class_='mtb-title').text
                   price = item.find('span',class_='sp_amt').text
                   weight = item.find('option',class_='VariantPropertyValue')
                   if weight==None:
                       weight=''
                   else:
                       weight=weight.text
                       weight=weight.replace(" ","")
                   product = {
                                    
                                    'name'   : name,
                                    'weight' : weight,
                                    'ty':'ty',
                                    'price'  : price,
                                    'description' : name,
                                    'link'   : plink,
                                    'source' : 'Simplinamdhari',
                                    'category':cat
                                    }
                   if(name not in product_name_list):
                       product_name_list.append(name)
                       productsList.append(product)
                       #print(product)
                          

    
    df=pd.DataFrame(productsList)
    column_names = ["name", "weight", "price","description","link","source","category"]
    df = df.reindex(columns=column_names)
    print(df.columns)
    df.to_csv(filename, mode='a', index=False, header=False)
    
def Simplinamdharis(fvfilename):
    
    smfruitveglist=['']*5
    smlist=['']*110
    
    smfruitveglist[0] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4118141,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224118141_CI84089111%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI84089111%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=163'
    smfruitveglist[1] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4118117,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224118117_CI68408991%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI68408991%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632211443052'
    smfruitveglist[2] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4117163,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224117163_CI68408983%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI68408983%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632211267814'
    smfruitveglist[3] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4117163,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224117163_CI68408983%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408983%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632503625690'
    smfruitveglist[4] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4118133,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224118133_CI84089105%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI84089105%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632211756598'
    smlist[0] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116847,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224116847_CI68408927%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI68408927%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632492104354'
    smlist[1] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116847,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116847_CI68408927%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408927%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632495430287'
    smlist[2] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116847,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116847_CI68408927%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408927%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632495595757'
    smlist[3] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116847,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116847_CI68408927%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408927%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632495948300'
    smlist[4] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116847,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:6,%22DivClientId%22:%224116847_CI68408927%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408927%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632496107153'
    smlist[5] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116855,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224116855_CI68408931%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI68408931%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632492282656'
    smlist[6] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116855,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116855_CI68408931%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408931%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632496264223'
    smlist[7] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116855,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116855_CI68408931%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408931%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632496366382'
    smlist[8] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116855,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116855_CI68408931%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408931%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632498345388'
    smlist[9] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116601,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116601_CI68408933%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408933%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632494759563'
    smlist[10] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116601,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116601_CI68408933%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408933%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632500195496'
    smlist[11] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116601,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116601_CI68408933%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408933%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632500395918'
    smlist[12] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116601,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116601_CI68408933%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408933%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632500664704'
    smlist[13] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116863,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116863_CI68408935%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408935%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632500811342'
    smlist[14] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116863,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116863_CI68408935%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408935%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632501006025'
    smlist[15] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116863,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116863_CI68408935%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408935%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632501371591'
    smlist[16] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116863,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116863_CI68408935%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408935%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632501539499'
    smlist[17] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116871,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224116871_CI68408937%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI68408937%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632501642732'
    smlist[18] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116871,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116871_CI68408937%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408937%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632501701765'
    smlist[19] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116871,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116871_CI68408937%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408937%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632501776911'
    smlist[20] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116871,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116871_CI68408937%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408937%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632501856488'
    smlist[21] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116871,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116871_CI68408937%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408937%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632501947804'
    smlist[22] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116871,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:6,%22DivClientId%22:%224116871_CI68408937%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408937%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632502068905'
    smlist[23] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116693,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116693_CI68408941%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408941%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632502264611'
    smlist[24] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116693,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116693_CI68408941%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408941%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632502361278'
    smlist[25] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116693,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116693_CI68408941%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408941%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632502978161'
    smlist[26] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116693,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116693_CI68408941%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408941%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632503075213'
    smlist[27] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116879,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224116879_CI68408945%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI68408945%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632503175356'
    smlist[28] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116879,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116879_CI68408945%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408945%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632503268050'
    smlist[29] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116895,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116895_CI84089157%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI84089157%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632503362859'
    smlist[30] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116895,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116895_CI84089157%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI84089157%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632503454136'
    smlist[31] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116895,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116895_CI84089157%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI84089157%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632503492814'
    smlist[32] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116625,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:6,%22DivClientId%22:%224116625_CI68408915%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408915%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996000540'
    smlist[33] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116625,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116625_CI68408915%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408915%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632995990804'
    smlist[34] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116625,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116625_CI68408915%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408915%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632995970486'
    smlist[35] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116625,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116625_CI68408915%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408915%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632995953925'
    smlist[36] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116553,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116553_CI68408913%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408913%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632996112638'
    smlist[37] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116553,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116553_CI68408913%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408913%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996368438'
    smlist[38] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116553,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116553_CI68408913%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408913%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996405674'
    smlist[39] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116553,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116553_CI68408913%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI68408913%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996436057'
    smlist[40] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632996636531'
    smlist[41] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996679678'
    smlist[42] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996683605'
    smlist[43] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996712282'
    smlist[44] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:6,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996717151'
    smlist[45] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:7,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996751996'
    smlist[46] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:8,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996759394'
    smlist[47] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:9,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996792725'
    smlist[48] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:10,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996814847'
    smlist[49] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:11,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996838305'
    smlist[50] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:12,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996847357'
    smlist[51] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:13,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996884657'
    smlist[52] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:14,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996892592'
    smlist[53] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:15,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996900148'
    smlist[54] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:17,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632996981298'
    smlist[55] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:18,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997004715'
    smlist[56] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:19,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997024510'
    smlist[57] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:20,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997044813'
    smlist[58] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:21,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997068776'
    smlist[59] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:22,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997077293'
    smlist[60] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:23,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997108676'
    smlist[61] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:24,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997129673'
    smlist[62] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:25,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997142827'
    smlist[63] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:26,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997175620'
    smlist[64] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:27,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997209585'
    smlist[65] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:28,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997227892'
    smlist[66] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:29,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997257938'
    smlist[67] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:30,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997287302'
    smlist[68] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:31,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997301922'
    smlist[69] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:32,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997333418'
    smlist[70] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:33,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997358618'
    smlist[71] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:34,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997411306'
    smlist[72] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:35,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997442690'
    smlist[73] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:36,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997474648'
    smlist[74] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:37,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997502093'
    smlist[75] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116465,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:38,%22DivClientId%22:%224116465_CI16840893%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840893%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1632997529144'
    smlist[76] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1632997582224'
    smlist[77] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001257848'
    smlist[78] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001273418'
    smlist[79] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001288371'
    smlist[80] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:6,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001406079'
    smlist[81] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:7,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001409279'
    smlist[82] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:8,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001410635'
    smlist[83] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:9,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001450189'
    smlist[84] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:10,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633001456164'
    smlist[85] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:11,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008303096'
    smlist[86] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:12,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008331245'
    smlist[87] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:13,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008341512'
    smlist[88] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:14,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008372938'
    smlist[89] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:15,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008445695'
    smlist[90] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:16,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008457639'
    smlist[91] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:17,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008488862'
    smlist[92] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:18,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008498579'
    smlist[93] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:19,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008536130'
    smlist[94] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:20,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008547182'
    smlist[95] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:21,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008619911'
    smlist[96] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:22,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008669455'
    smlist[97] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:23,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008696559'
    smlist[98] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4116585,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:24,%22DivClientId%22:%224116585_CI16840895%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI16840895%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633008734474'
    smlist[99] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4117103,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:1,%22DivClientId%22:%224117103_CI84089177%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:true,%22CID%22:%22CI84089177%22,%22CT%22:0,%22TabId%22:0,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1633009314336'
    smlist[100] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4117103,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224117103_CI84089177%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%22CI84089177%22,%22CT%22:0,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633009897244'
    smlist[101] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:2,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22A%22}&_=1633009943938'
    smlist[102] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:3,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633009985448'
    smlist[103] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:4,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633009999316'
    smlist[104] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:5,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633010017181'
    smlist[105] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:6,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633010031222'
    smlist[106] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:7,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633010045854'
    smlist[107] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:8,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633010065608'
    smlist[108] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:9,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633010085391'
    smlist[109] = 'https://www.simplinamdharis.com/Handler/ProductShowcaseHandler.ashx?ProductShowcaseInput={%22PgControlId%22:4119915,%22IsConfigured%22:true,%22ConfigurationType%22:%22%22,%22CombiIds%22:%22%22,%22PageNo%22:10,%22DivClientId%22:%224119915_1406293%22,%22SortingValues%22:%22CS%22,%22ShowViewType%22:%22H%22,%22PropertyBag%22:null,%22IsRefineExsists%22:false,%22CID%22:%221406293%22,%22CT%22:3,%22TabId%22:%220%22,%22LocationIds%22:%2229935%22,%22CurrencyCode%22:%22INR%22,%22ContentType%22:%22B%22,%22PageMultiplier%22:1}&_=1633010102246'   
    for i in range(len(smfruitveglist)):
        SimplinamdhariScrapeData(smfruitveglist[i],fvfilename,category[0])
    
    for i in range(len(smlist)):
        #print(i)
        SimplinamdhariScrapeData(smlist[i],fvfilename,category[1])


def TownessScrpadeData(link,header,filename,cat):
    r = requests.get(link,headers=header)
    #soup_object = soup(r.content)
    data = json.loads(r.text)
    #print(data)
    productlist=[]
    for each in data:
        urlpart1=each['a']
        urlpart2=each['b']
        urlpart3=str(each['c'].lower())
        urlpartf=urlpart3.replace(' ','-')
        url='https://towness.co.in/web/product/'+urlpart1+'/'+urlpart2+'/'+urlpartf
        weig=each['j']+each['k']
        weig=weig.replace(" ","")
        product={
                    'name':each['c'],
                    'weight':weig,
                    'price':each['d'],
                    'description':each['c'],
                    'link':url,
                    'source':"Towness",
                    'category':cat
                    
                    #'mrp':each['e'],
                    #'dis_val':dis_val[i],
                    #'img_url':each['m'],
                    
                }
        productlist.append(product)
        
    #print(len(productlist))
    #for i in range(len(productlist)):
        #print(i,productlist[i]['name'])
    
    
    df=pd.DataFrame(productlist)
    column_names = ["name", "weight", "price","description","link","source","category"]
    df = df.reindex(columns=column_names)
    print(df.columns)
    df.to_csv(filename,mode='a',index=False,header=False)
        
        
def Towness(fvfilename):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    
    """fruitfile='FruitsTowness.csv'
    f=open(fruitfile,"w+")
    f.close()"""
    Fruit_req="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=367&endcount=199&startcount=0&type=category"
    TownessScrpadeData(Fruit_req,header,fvfilename,category[0])
    
    """vegetablesfile='VegetablesTowness.csv'
    f=open(vegetablesfile,"w+")
    f.close()"""
    Veg_req="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=363&endcount=199&startcount=0&type=category"
    TownessScrpadeData(Veg_req,header,fvfilename,category[0])
    
    """groceryfile='GroceryTowness1.csv'
    f=open(groceryfile,"w+")
    f.close()"""
    
    grocerylist=[""]*20
    grocerylist[0]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=639&endcount=199&startcount=0&type=category"
    grocerylist[1]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=637&endcount=199&startcount=0&type=category"
    grocerylist[2]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=736&endcount=199&startcount=0&type=category"
    grocerylist[3]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=631&endcount=199&startcount=0&type=category"
    grocerylist[4]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=629&endcount=199&startcount=0&type=category"
    grocerylist[5]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=569&endcount=199&startcount=0&type=category"
    grocerylist[6]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=565&endcount=199&startcount=0&type=category"
    grocerylist[7]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=403&endcount=199&startcount=0&type=category"
    grocerylist[8]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=732&endcount=199&startcount=0&type=category"
    grocerylist[9]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=548&endcount=199&startcount=0&type=category"
    grocerylist[10]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=406&endcount=199&startcount=0&type=category"
    grocerylist[11]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=560&endcount=199&startcount=0&type=category"
    grocerylist[12]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=694&endcount=199&startcount=0&type=category"
    grocerylist[13]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=547&endcount=199&startcount=0&type=category"
    grocerylist[14]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=734&endcount=199&startcount=0&type=category"
    grocerylist[15]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=633&endcount=199&startcount=0&type=category"
    grocerylist[16]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=733&endcount=199&startcount=0&type=category"
    grocerylist[17]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=722&endcount=199&startcount=0&type=category"
    grocerylist[18]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=408&endcount=199&startcount=0&type=category"
    grocerylist[19]="https://towness.co.in/xcart44/mobileapiv20/getprodpaginatedapiv10.php?categoryid=564&endcount=199&startcount=0&type=category"

    
    for i in range(len(grocerylist)):
        TownessScrpadeData(grocerylist[i],header,fvfilename,category[1])
    
    



def EztrolleyScrapeData(rlink,header,filename,cat):
    #print(soup)
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    #chromedriver_path= "C:/Users/Apsara/Documents/chromedriver.exe"
    #driver = webdriver.Chrome(chromedriver_path)
    #chromedriver_path= "C:/Users/Apsara/Documents/chromedriver.exe"
    #driver = webdriver.Chrome(chromedriver_path)
    #driver.get(rlink)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #time.sleep(3) #if you want to wait 3 seconds for the page to load
    
    driver.get(rlink)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3) #if you want to wait 3 seconds for the page to load
    page_source = driver.page_source
    soup_ez = soup(page_source, 'lxml')
    p=soup_ez.find_all('div',class_="productWrap")
    #print(p)
    product_name_list=[]
    productsList=[]
    for item in p:
        for link in item.find_all('a',href=True):
                plink = link['href']
                
                name = link.text.strip()
                weight = item.find('span',class_='list_weight center').text
                price = item.find('span',class_='ezprice right').text.strip()
                product_name_list.append(name)
                
                #productsList.append(product)
                if(plink!='#'):
                   """r1 = requests.get(plink,headers=headers)
                   print(plink,r1)
                   soup2 = BeautifulSoup(r1.text, 'html.parser')
                   desc = soup2.find('div',class_='prod_desc')
                   if desc == None:
                        desc = name
                   else :
                        desc = soup.find('div',class_='prod_desc').text
                        print(desc)"""
                   print(plink)
                   weight=weight.replace(" ","")
                   product = {
                        
                        'name'   : name,
                        'weight' : weight,
                        'price'  : price,
                        'description' : name,
                        'link'   : plink,
                        'source' : "Eztrolley",
                        'category':cat}
                   if(name!=''):
                       productsList.append(product)
                #print(product)
    #print(productsList)
    #print(len(productsList))
    
    df=pd.DataFrame(productsList)
    column_names = ["name", "weight", "price","description","link","source","category"]
    df = df.reindex(columns=column_names)
    print(df.columns)
    df.to_csv(filename, mode='a', index=False, header=False)

def eztrolley(fvfilename):
    fruits = 'http://www.eztrolley.com/shopping/buy-fruits-online-store-bangalore'
    veggies = 'http://www.eztrolley.com/shopping/online-vegetables-shopping-bangalore'
    veggies_exotic = 'http://www.eztrolley.com/shopping/online-exotic-vegetables-shop-bangalore'

    EztrolleyScrapeData(fruits,header,fvfilename,category[0])
    EztrolleyScrapeData(veggies,header,fvfilename,category[0])
    EztrolleyScrapeData(veggies_exotic,header,fvfilename,category[0])

       
def jiomartScrapeData(vlink,header,filename,pg,cat):
    productsList=[]
    #vlink = 'https://www.jiomart.com/c/groceries/staples/masalas-spices/21/page/'
    for x in range(1,pg):
        rlink = vlink + str(x)
        print(rlink)
        baseurl='https://www.jiomart.com/'
        r = requests.get(rlink,headers=header)
        #print(r)
        #soup = BeautifulSoup(r.content, 'lxml')
        soup_jio_data = soup(r.text,'html.parser')
        #print(soup)
        #p=soup.find_all('div',class_="col-md-3 p-0")
        #p1 = soup.find_all(id="final_price")
        #print(p1)
        p=soup_jio_data.find_all('div',class_="cat-item")
        #print(p)
        
        for item in p:
            #for pr in item.find('span',class_='price-box'):
                #print(pr)
            for link in item.find_all('a',href=True):
                #print(link['href'])
                plink = baseurl + link['href']
                print(plink)
                #productlinks.append(plink)
                
                r = requests.get(plink, headers=header)
                prod_soup = soup(r.content,'lxml')
                name = prod_soup.find('div',class_='title-section').text            
                #tax = prod_soup.find('span',class_='tax_text').text
                desc = prod_soup.find('div',class_='feat_detail').text
                #seller = prod_soup.find('div',class_='seller_details').text
            mrp = item.find('span',class_='price-box')
            price = mrp.find(id='final_price')
            price=price.text
            price1=price.replace("â‚¹","" )
            #print(price1)
            product = {
                        
                        'name'   : name,
                        'weight' : '',
                        'price'  : price1,
                        'description' : desc,
                        'link'   : plink,
                        'source' : "JioMart",
                        'category':cat
                        
                        
                        }
            productsList.append(product)
   
    df=pd.DataFrame(productsList)
    column_names = ["name", "weight", "price","description","link","source","category"]
    df = df.reindex(columns=column_names)
    print(df.columns)
    df.to_csv(filename, mode='a', index=False, header=False)

    
def jiomart(fvfilename):
    
    jiofruitsveglink=['']*3
    jiogrocerylink=['']*27
    
    jiofruitsveglink[0] = 'https://www.jiomart.com/c/groceries/fruits-vegetables/fresh-fruits/220/page/'
    jiofruitsveglink[1] = 'https://www.jiomart.com/c/groceries/fruits-vegetables/fresh-vegetables/229/page/'    
    #herbs_seasoning = 'https://www.jiomart.com/c/groceries/fruits-vegetables/herbs-seasonings/233/page/' 
    jiofruitsveglink[2] = 'https://www.jiomart.com/c/groceries/fruits-vegetables/exotic-fruits-vegetables/243/page/'
    
    jiogrocerylink[0] = 'https://www.jiomart.com/c/groceries/staples/atta-flours-sooji/26/page/'    
    jiogrocerylink[1] = 'https://www.jiomart.com/c/groceries/staples/dals-pulses/17/page/'
    jiogrocerylink[2] = 'https://www.jiomart.com/c/groceries/staples/rice-rice-products/14/page/'
    jiogrocerylink[3] = 'https://www.jiomart.com/c/groceries/staples/edible-oils/58/page/'
    jiogrocerylink[4] = 'https://www.jiomart.com/c/groceries/staples/masalas-spices/21/page/'
    jiogrocerylink[5] = 'https://www.jiomart.com/c/groceries/staples/salt-sugar-jaggery/23/page/'
    jiogrocerylink[6] = 'https://www.jiomart.com/c/groceries/staples/soya-products-wheat-other-grains/106/page/'
    jiogrocerylink[7] = 'https://www.jiomart.com/c/groceries/staples/dry-fruits-nuts/657/page/'
    jiogrocerylink[8] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/noodle-pasta-vermicelli/86/page/' #9
    jiogrocerylink[9] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/breakfast-cereals/98/page/' #10
    jiogrocerylink[10] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/snacks-namkeen/43/page/'#26
    jiogrocerylink[11] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/chocolates-candies/70/page/' #13
    jiogrocerylink[12] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/ready-to-cook-eat/53/page/' #23
    jiogrocerylink[13] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/frozen-veggies-snacks/111/page/' #2
    jiogrocerylink[14] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/spreads-sauces-ketchup/55/page/' #23
    jiogrocerylink[15] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/indian-sweets/46/page/' #7
    jiogrocerylink[16] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/pickles-chutney/51/page/' #8
    jiogrocerylink[17] = 'https://www.jiomart.com/c/groceries/snacks-branded-foods/extracts-flavouring/181/page/' #2
    jiogrocerylink[18] = 'https://www.jiomart.com/c/groceries/beverages/tea/34/page/' #12
    jiogrocerylink[19] = 'https://www.jiomart.com/c/groceries/beverages/coffee/94/page/' #4
    jiogrocerylink[20] = 'https://www.jiomart.com/c/groceries/beverages/energy-soft-drinks/40/page/' #7
    jiogrocerylink[21] = 'https://www.jiomart.com/c/groceries/beverages/health-drink-supplement/49/page/' #5
    jiogrocerylink[22] = 'https://www.jiomart.com/c/groceries/beverages/soda-flavoured-water/115/page/' #3
    jiogrocerylink[23] = 'https://www.jiomart.com/c/groceries/dairy-bakery/dairy/62/page/' #6
    jiogrocerylink[24] = 'https://www.jiomart.com/c/groceries/dairy-bakery/cheese/1569/page/' #4
    jiogrocerylink[25] = 'https://www.jiomart.com/c/groceries/dairy-bakery/ghee/1571/page/' #3
    jiogrocerylink[26] = 'https://www.jiomart.com/c/groceries/dairy-bakery/paneer-tofu/1573/page/' #2
    
    JM_pagenosfruitsveg = [3, 4, 3]
    
    JM_pagenosgrocery=[ 7, 7, 7, 7, 9, 7, 3, 13, 9, 10, 26, 13, 23, 2, 23, 7, 8, 2, 12, 4, 7, 5, 3, 6, 4, 3, 2]
    
    for i in range(len(jiofruitsveglink)):
        jiomartScrapeData(jiofruitsveglink[i],header,fvfilename,JM_pagenosfruitsveg[i],category[0])
        
    #for i in range(len(jioveggieslink)):
        #jiomartScrapeData(jioveggieslink[i],header,grcyfilename,JM_pagenosveggies[i])
    for i in range(len(jiogrocerylink)):
        jiomartScrapeData(jiogrocerylink[i],header,fvfilename,JM_pagenosgrocery[i],category[1])

                
    
    
if __name__=="__main__":
    
    
    
    
    #Fruits and Vegetables File
    #FruitsVegetablesFile='Fruits_VegetablesData.csv'
    #ffv=open(FruitsVegetablesFile,"w+")
    #ffv.close()

    
    #Grocery File
    GroceryFile='ProductsDataFinal.csv'
    fg=open(GroceryFile,"w+")
    fg.close()
    #print(category[0])
    #Simplinamdhari's
    Simplinamdharis('ProductsDataFinal.csv')
    
    
    #Towness
    #Towness('ProductsData.csv')
    
    
    
    #BigBasket
    BigBasket('ProductsDataFinal.csv')
    
    #jiomart
    jiomart('ProductsDataFinal.csv')
    
    #eztrolley
    eztrolley('ProductsDataFinal.csv')
    
    
