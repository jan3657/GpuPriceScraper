import requests
from lxml import html

#Num of gpus
numOfGpus = 1

#Websites
websites = ['notebooksbilliger','caseking']

notebooksbilligerUrl1 = 'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/geforce+rtx+'
notebooksbilligerUrl2 = '+nvidia/page/1?sort=price&order=asc&availability=alle'
notebooksbilligerProducts = {'3090':'3090',
                             '3080ti':'3080+ti',
                             '3080':'3080',
                             '3070ti':'3070+ti',
                             '3070':'3070'}

casekingUrl1= 'https://www.caseking.de/en/pc-components/graphics-cards/nvidia/geforce-rtx-'
casekingUrl2= '?sSort=3&sPage=1&sPerPage=48'
casekingProducts = {'3090':'3090',
                    '3080ti':'3080-ti',
                    '3080':'3080',
                    '3070ti':'3070-ti',
                    '3070':'3070'}

#requests headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept-Encoding': None
}


#def check_price():
#    url = 'https://www.notebooksbilliger.de/msi+geforce+rtx+3070+ti+ventus+3x+oc+8gb+gddr6x+grafikkarte+720467/eqsqid/7f61cf5d-13f9-46b6-bcf1-ebd9301113ce'
#
#    response = requests.get(url, headers=headers)
#    tree = html.fromstring(response.content)
#    price = tree.xpath('//div[@id="product_detail_price"]/div[@class="product-price__wrapper"]/span[@class="product-price__regular js-product-price"]/text()')[0]
#    print(price.split()[0])

def check_prices(websites):
    shoopsPrices = {}

    for website in websites:  
        cards = {}
        products = eval(website+"Products")

        for product in products:
            url = eval(website+"Url1")+products[product]+eval(website+"Url2")
            response = requests.get(url, headers=headers)
            tree = html.fromstring(response.content)     

            names = eval(website + "_names(tree)")
            prices = eval(website + "_prices(tree)")
            #caseking_stock(tree)

            for n in range(0,numOfGpus):
                

                info = {
                    "name": names[n].strip(),
                    "price": prices[n]
                }
                cards[product]=info

        shoopsPrices[website]=cards

    return shoopsPrices


                

def notebooksbilliger_prices(tree):
    prices = tree.xpath('//span[@class="product-price__regular js-product-price"]/text()')
    prices = [s.strip() for s in prices]
    prices = [s.replace(" €","") for s in prices]
    return prices          

def notebooksbilliger_names(tree):
    names = tree.xpath('//a [@class="listing_product_title"]/text()')
    return names  

def notebooksbilliger_stock(tree):
    stock = tree.xpath('//span [@class="highlight_green"]/text()')
    stock = [s.replace("sofort ab Lager","immediately available ") for s in stock]
    return stock  
    
def caseking_prices(tree):
    prices = tree.xpath('//span[@class="price"]/text()')
    prices = [s.replace("€*", "") for s in prices]
    return prices    

def caseking_names(tree):
    prices = tree.xpath('//span[@class="ProductTitle"]/text()')
    return prices   

def caseking_stock(tree):
    stock = tree.xpath('//span [@class="delivery_container"]')
    for i in stock:
        print(i.tag)
    #print(type(stock))
    #stock = [s.replace("sofort ab Lager","immediately available ") for s in stock]
    return stock  

if __name__ == "__main__":
    #print("%20s \n %10s " % ("whazap","Niggas"))

    prices = check_prices(websites)

    for i in prices:
        print("%-3s %s" % (" ",i) )
        for j in prices[i]:
            print("%-10s %s€" %(j, prices[i][j].get('price')))        

        print("")