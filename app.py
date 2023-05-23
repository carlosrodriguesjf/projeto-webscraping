

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=1200,920', '--incognito']
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

# 1 - Conectar no site  https://telefonesimportados.netlify.app  e selecionar o nome do celular e o preço em todas as páginas

driver = iniciar_driver()
driver.get('https://telefonesimportados.netlify.app')
sleep(3)

proxima_pagina = driver.find_element(By.XPATH,"//li/a[@aria-label='Next']")

while True:

    if proxima_pagina != '':

        for i in range(12):
            nomes = driver.find_elements(By.XPATH,'//div//h2/a')
            nome = print(nomes[i].text)
            precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")
            preco = print(precos[i].text.split('$')[1])
            sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        proxima_pagina.click()
        sleep(5)













input('tecle algo para fechar')




















































#2 - Salvar  os dados em uma planilha 




#3 - enviar a planilha poe e-mail