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

while True:
    driver.execute_script("window.scrollTo(0, 1200);")
    for i in range(0,len(nomes)):
        try:
            proxima_pagina = driver.find_element(By.XPATH,"//li/a[@aria-label='Next']")
            nomes = driver.find_elements(By.XPATH,'//div//h2/a')
            precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")
            nome = nomes[i].text
            preco = precos[i].text.split('$')[1]
            print('Guardando valores da página atual...')
            sleep(2)
        except:
            proxima_pagina = driver.find_element(By.XPATH,"//li/a[@aria-label='Next']")
        finally:
            nomes = driver.find_elements(By.XPATH,'//div//h2/a')
            precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")
            nome = nomes[i].text
            preco = precos[i].text.split('$')[1]
    print('\nIndo para a próxima página\n')
    proxima_pagina.click()
    sleep(1)
    driver.execute_script("window.scrollTo(0, 1200);")

    print('Fim do programa')
    break
    sleep(5)

  
driver.close()