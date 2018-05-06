import csv
import requests
from bs4 import BeautifulSoup
import time


filename = "main2.csv"
f = open(filename, "w",encoding="utf-8")
headers = " Brand/Seller, Product_Name, Price, SKU/ID , Category Flow \n"
f.write(headers)



prime_url = "https://www.daraz.com.bd/"
while True:
    try:
        resource = requests.get(prime_url).text
        break
    except:
        print("wait for 10 sec folk")
        time.wait(10)
soup = BeautifulSoup(resource,"html.parser")
list = soup.findAll("li",{"class":"menu-item"})
cat_list_urls = []
brand_urls = []
brand_names = []
for i in range(len(list)):
    cat_list = list[i].findAll("a",{"class":"category"})
    for i in range(len(cat_list)):
        cat_list_urls.append(cat_list[i]['href'])
#print(cat_list_urls)   #every catagory url is in this array,

for i in range(len(cat_list_urls)-1):
    cat_list_url = cat_list_urls[i];  #cat_list_url[0] means men fashion's western category , should be cat_list_urls[i]
    if( cat_list_url == "https://www.daraz.com.bd/womens-clothing-top-brands/" or cat_list_url == "https://www.daraz.com.bd/womens-fashion/?sort=newest&dir=desc" or cat_list_url == "https://www.daraz.com.bd/womens-fashion/?special_price=1"):
        continue
    else:
        while True:
            try:
                cat_resource = requests.get(cat_list_url).text
                break
            except:
                print("wait for 10 sec folk")
                time.wait(10)

        cat_soup = BeautifulSoup(cat_resource,"html.parser")

        brand_article = cat_soup .findAll("article",{"class":"ft-vertical-filter-brand"})
        brand_div = brand_article[0].findAll("div",{"class":"-facet"})
        brand_anchor = brand_div[0].findAll("a",{"class":"facet-link"})  #brand_anchor is an array of anchor tags containing the urls and names, under the MEN>WESTERN CATEGORY

        for i in range(len(brand_anchor)-1):
            brand_urls.append(brand_anchor[i]['href'])
            brand_names.append(brand_anchor[i]['title'])

        for i in range(len(brand_urls)-1):
            brand_url =  brand_urls[i]
            for i in range(25+1):
                page_string = "?page="
                url = brand_url + page_string + str(i+1)
                print(url)

                while True:
                    try:
                        resource = requests.get(url).text
                        break
                    except:
                        print("wait for 10 sec folk")
                        time.wait(10)

                soup = BeautifulSoup(resource,"html.parser")
                chronology = soup.findAll("nav",{"class":"osh-breadcrumb"})



                if(len(chronology) ==0 ) :
                    break


                cat_flow_section = soup.findAll("section",{"class":"products"})
                cat_flow_div = cat_flow_section[0].findAll("div",{"class":"-gallery"})
                cat_flow_link = []
                for i in range(len(cat_flow_div)):
                    cat_flow_link.append(cat_flow_div[i].a['href'])



                ulist_item = chronology[0].ul

                b = ulist_item.findAll("li",{"class":"last-child -brand"})
                brand = b[0].a.contents
                print("brand: " +brand[0])  #######################################################


                products = soup.findAll("a",{"class":"link"})

                for i in range(len(products)):
                    product = products[i].h2
                    n = product.findAll("span",{"class":"name"})
                    product_name = n[0].contents
                    print("product_name: " +product_name[0])   ##################################################

                    price_container = products[i].findAll("div",{"class":"price-container"})
                    span_class_price = price_container[0].findAll("span",{"class":"price-box"})
                    span_tags = span_class_price[0].span.find_all('span')
                    spantag_data_price = span_tags[1]
                    price = spantag_data_price['data-price']
                    print("price: " +price) #################################################

                    id_holder = products[i].div
                    id = id_holder.img['data-sku']
                    print("id: " + id)    #########################################

                    while True:
                        try:
                            cat_flow_resource = requests.get(cat_flow_link[i]).text
                            break
                        except:
                            print("wait for 10 sec folk")
                            time.wait(10)
                    cat_flow_soup = BeautifulSoup(cat_flow_resource,"html.parser")
                    cat_flow_nav = cat_flow_soup.findAll("nav",{"class":"osh-breadcrumb"})
                    cat_nav_ul = cat_flow_nav[0].ul
                    cat_nav_li = cat_nav_ul.findAll("li",{"class":""})
                    flow_names = " "
                    for i in range(len(cat_nav_li)-1):
                        flow = cat_nav_li[i].a.contents
                        flow_names = flow_names+ flow[0] +">"
                    print(flow_names)  ##############################################

                    f.write(''.join(brand + [","] + product_name + [","] +[price] + [","] + [id] + [","] + [flow_names] +[","] + ["\n"]) )

f.close()
