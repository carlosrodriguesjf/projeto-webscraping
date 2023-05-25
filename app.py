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
sheet_celulares.append(['Marca','Preço'])


# Montagem do e-mail
EMAIL_ADDRESS_SEND = input('Digite para qual e-mail a planilha deve ser encaminhada: ')

EMAIL_ADDRESS = 'carlosrodriguesjfprojetos@gmail.com'
EMAIL_PASSWORD = 'kkoabxdhtyucdmql'

mail = EmailMessage()
mail['Subject'] = 'Seu relatório de preços'
mensagem = 'Baixe seu relatório de preços de celular agora!'

mail['From'] = EMAIL_ADDRESS
mail['To'] = EMAIL_ADDRESS_SEND
mail.add_header('Content-Type', 'text/html')
mail.set_payload(mensagem.encode('ISO-8859-1'))




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


driver = iniciar_driver()
driver.get('https://telefonesimportados.netlify.app')
sleep(3)

proxima_pagina = driver.find_element(By.XPATH,"//li/a[@aria-label='Next']")
nomes = driver.find_elements(By.XPATH,'//div//h2/a')
precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")

while True:
    try:                                        
        driver.execute_script("window.scrollTo(0, 1200);")
        for i in range(0,len(nomes)):
            nomes = driver.find_elements(By.XPATH,'//div//h2/a')
            precos = driver.find_elements(By.XPATH,"//div[@class='product-carousel-price']/ins")
            nome = nomes[i].text
            preco = precos[i].text.split('$')[1]
            sheet_celulares.append([nome,preco])
            print('Guardando valores da página atual...')
            sleep(2)       
        sleep(1)
        proxima_pagina = driver.find_element(By.XPATH,"//li/a[@aria-label='Next']")
        proxima_pagina.click()
        print('\nIndo para a próxima página\n')
    except:   
        break


workbook.save('valores_celulares_importados.xlsx')
print('Enviando e-mail...')

arquivos = ['valores_celulares_importados.xlsx']

for arquivo in arquivos:
    with open(arquivo, 'rb') as arquivo:
        dados = arquivo.read()
        nome_arquivo = arquivo.name
        mail.add_attachment(dados, maintype='application',
                            subtype='octet-stream', filename='valores_celulares_importados.xlsx')


with smtplib.SMTP_SSL('smtp.gmail.com',465) as email:
    email.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    email.send_message(mail)


    print('E-mail enviado com sucesso...')

driver.close()


