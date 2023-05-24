# PROJETO 3 - VARREDURA DE SITE E-COMMERCE + ARMAZENAMENTO EM PLANILHA - WEB SCRAPING

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import openpyxl
import smtplib
from email.message import EmailMessage


# Montagem da planilha
workbook = openpyxl.Workbook()
workbook.create_sheet('Celulares')
del workbook['Sheet']
sheet_celulares = workbook['Celulares']
sheet_celulares.append(['Celular','Preço'])

def varre_pagina(proxima_pagina,nomes,precos):
    proxima_pagina = driver.find_element(By.XPATH,"//li/a[@aria-label='Next']")
    nomes = driver.find_elements(By.XPATH,'//div//h2/a')
    precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")
    nome = nomes[i].text
    preco = precos[i].text.split('$')[1]
    sheet_celulares.append([nome,preco])
    print('Guardando valores da página atual...')
    sleep(1)
    return proxima_pagina,nome,preco



def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1420,820', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,

    })
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)

    return driver



# 1 - Conectar no site https://telefonesimportados.netlify.app  e selecionar o nome do celular e o preço em todas as páginas

driver = iniciar_driver()
driver.get('https://telefonesimportados.netlify.app')
sleep(3)

proxima_pagina = driver.find_element(By.XPATH,"//li/a[@aria-label='Next']")
nomes = driver.find_elements(By.XPATH,'//div//h2/a')
precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")

while proxima_pagina:

    driver.execute_script("window.scrollTo(0, 1200);")
    for i in range(0,len(nomes)):
        proxima_pagina, teste1, teste2 = varre_pagina(proxima_pagina,nomes,precos)
    driver.execute_script("window.scrollTo(0, 1200);")
    sleep(3)
    print('\nIndo para a próxima página\n')
    sleep(2)
    nomes = driver.find_elements(By.XPATH,'//div//h2/a')
    precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")
    nome = nomes[i].text
    preco = precos[i].text.split('$')[1]
    sheet_celulares.append([nome,preco])
    sleep(1)
    proxima_pagina.click()

    



driver.close()
