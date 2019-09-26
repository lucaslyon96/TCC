#!/usr/bin/env python3
import re
import urllib.request
import urllib.parse
import http.cookiejar
import pandas as pd 
from lxml.html import fragment_fromstring
from collections import OrderedDict
import csv
from datetime import date
from datetime import datetime
import numpy as np
def get_data(*args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min':'',
            'pl_max':'',
            'pvp_min':'',
            'pvp_max' :'',
            'psr_min':'',
            'psr_max':'',
            'divy_min':'',
            'divy_max':'',
            'pativos_min':'',
            'pativos_max':'',
            'pcapgiro_min':'',
            'pcapgiro_max':'',
            'pebit_min':'',
            'pebit_max':'',
            'fgrah_min':'',
            'fgrah_max':'',
            'firma_ebit_min':'',
            'firma_ebit_max':'',
            'margemebit_min':'',
            'margemebit_max':'',
            'margemliq_min':'',
            'margemliq_max':'',
            'liqcorr_min':'',
            'liqcorr_max':'',
            'roic_min':'',
            'roic_max':'',
            'roe_min':'',
            'roe_max':'',
            'liq_min':'',
            'liq_max':'',
            'patrim_min':'',
            'patrim_max':'',
            'divbruta_min':'',
            'divbruta_max':'',
            'tx_cresc_rec_min':'',
            'tx_cresc_rec_max':'',
            'setor':'',
            'negociada':'ON',
            'ordem':'1',
            'x':'28',
            'y':'16'}

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    reg = re.findall(pattern, content)[0]
    page = fragment_fromstring(reg)
    lista = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        lista.update({rows.getchildren()[0][0].getchildren()[0].text: {'cotacao': rows.getchildren()[1].text,
                                                                       'P/L': rows.getchildren()[2].text,
                                                                       'P/VP': rows.getchildren()[3].text,
                                                                       'PSR': rows.getchildren()[4].text,
                                                                       'DY': rows.getchildren()[5].text,
                                                                       'P/Ativo': rows.getchildren()[6].text,
                                                                       'P/Cap.Giro': rows.getchildren()[7].text,
                                                                       'P/EBIT': rows.getchildren()[8].text,
                                                                       'P/Ativ.Circ.Liq.': rows.getchildren()[9].text,
                                                                       'EV/EBIT': rows.getchildren()[10].text,
                                                                       'EBITDA': rows.getchildren()[11].text,
                                                                       'Mrg.Liq.': rows.getchildren()[12].text,
                                                                       'Liq.Corr.': rows.getchildren()[13].text,
                                                                       'ROIC': rows.getchildren()[14].text,
                                                                       'ROE': rows.getchildren()[15].text,
                                                                       'Liq.2m.': rows.getchildren()[16].text,
                                                                       'Pat.Liq': rows.getchildren()[17].text,
                                                                       'Div.Brut/Pat.': rows.getchildren()[18].text,
                                                                       'Cresc.5a': rows.getchildren()[19].text}})
    
    return lista
    
if __name__ == '__main__':
    #from waitingbar import WaitingBar
    #THE_BAR = WaitingBar('[*] Downloading...')
    lista = get_data()
    #THE_BAR.stop()
    lis= [["Papel","Cotação","P/L","P/VP","PSR","DY(%)",'P/Ativo','P/Cap.Giro',"P/EBIT",'P/Ativ.Circ.Liq.',
    		"EV/EBIT","EBITDA(%)","Mrg.Liq.(%)","Liq.Corr.","ROIC(%)","ROE(%)",'Liq.2m.','Pat.Liq',
    		"Div.Brut/Pat.","Cresc.5a(%)"]]
    for k, v in lista.items():
        lis.append([k,(v['cotacao'].replace(".","")).replace(",","."),(v['P/L'].replace(".","")).replace(",","."),(v['P/VP'].replace(".","")).replace(",",".")
        	,(v['PSR'].replace(".","")).replace(",","."),((v['DY'].replace(".","")).replace(",",".")).replace("%",""),(v['P/Ativo'].replace(".","")).replace(",",".")
        	,(v['P/Cap.Giro'].replace(".","")).replace(",","."),(v['P/EBIT'].replace(".","")).replace(",","."),(v['P/Ativ.Circ.Liq.'].replace(".","")).replace(",",".")
        	,(v['EV/EBIT'].replace(".","")).replace(",","."),((v['EBITDA'].replace(".","")).replace(",",".")).replace("%",""),((v['Mrg.Liq.'].replace(".","")).replace(",",".")).replace("%",""),
        	(v['Liq.Corr.'].replace(".","")).replace(",","."),((v['ROIC'].replace(".","")).replace(",",".")).replace("%",""),((v['ROE'].replace(".","")).replace(",",".")).replace("%",""),
        	(v['Liq.2m.'].replace(".","")).replace(",","."),(v['Pat.Liq'].replace(".","")).replace(",","."),(v['Div.Brut/Pat.'].replace(".","")).replace(",","."),((v['Cresc.5a'].replace(".","")).replace(",",".")).replace("%","")])	
    df=pd.DataFrame(lis)
    print(datetime.now())
    df['data']=datetime.now()
    df.to_csv('/home/lucas/Documentos/UFRN/Tcc/TCC/fundamentus-master/data_acoes/data_{}.csv'.format(datetime.now()),index=False,header=False)
   