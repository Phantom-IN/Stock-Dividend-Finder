import math
import requests
from bs4 import BeautifulSoup


def DivYield(com, retn):
    print('\nYou chose--> ', com)
    r1 = requests.get('https://ticker.finology.in/GetSearchData.ashx?q=' + com,
                      headers={'X-Requested-With': 'XMLHttpRequest'})
    res2 = r1.text
    FinCode = res2.split('"FINCODE":')
    scrip = FinCode[1].split(',')
    r2 = requests.get('https://ticker.finology.in/company/SCRIP-' + scrip[0])
    soup = BeautifulSoup(r2.content, 'html.parser')
    div = soup.findAll('div', class_='col-6 col-md-4 compess')
    divYield = div[6].text
    refine = list(divYield.strip().replace(' ', ''))
    str1 = ''
    for j in refine:
        str1 += j
    lst = str1.split("\n")
    print('\n[*] The dividend yielded per share was', lst[2])
    dividend = float(lst[2].replace('%', ''))
    div2 = soup.find('div', id='mainContent_clsprice')
    p = div2.text
    lstPrice = p.split('\n')
    price = float(lstPrice[2])
    if dividend > 0:

        divPerShare = (dividend * price)/100
        noOfShare = retn/divPerShare
        totalInvest = math.ceil(noOfShare*price)
        print('[*] Inorder to get ', retn, 'in dividend you will need to invest ', totalInvest, ' rupees in total.')
    else:
        print('\nCannot estimate the returns!')


if __name__ == '__main__':
    returns = int(input('How much returns do you want? --> '))
    company = input('\nEnter the company name--> ')
    r = requests.get('https://ticker.finology.in/GetSearchData.ashx?q=' + company,
                     headers={'X-Requested-With': 'XMLHttpRequest'})
    res = r.json()
    j = 1
    sResults = {}
    for i in res:
        cname = str(i)
        name = cname.replace("{'compname': '", '')
        finalName = name.split("',", 1)
        sResults[j] = finalName[0]
        j += 1

    if len(sResults) == 1:
        company = sResults.get(1)
        DivYield(company, returns)
    else:
        for key, value in sResults.items():
            print('[', key, ']', '', value)
        choice = int(input('\nWhich company you want to invest in? (Enter the number)--> '))
        company = sResults.get(choice)
        DivYield(company, returns)
