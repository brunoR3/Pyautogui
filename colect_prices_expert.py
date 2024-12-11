import pyautogui
import time
import os

# Caminho do ERP
erp_path = r'C:\Atx\AtxExec.exe'

# Passo 1: Abrir o ERP
os.startfile(erp_path)

# Aguardar alguns segundos para garantir que o ERP carregue
time.sleep(10)

# Passo 2: Mover o mouse e clicar no campo de login
# Substitua os valores (x, y) pelas coordenadas do campo de login
pyautogui.click(x=808, y=588)  # Coordenadas do campo de login
pyautogui.write('user') 

# Aguarda um momento
time.sleep(5)

# Substitua os valores (x, y) pelas coordenadas do campo de senha
pyautogui.click(x=809, y=634)  # Coordenadas do campo de senha
pyautogui.write('senha')    # Digitar a senha

# Aguarda um momento
time.sleep(5)

# Passo 4: Pressionar Enter para fazer login repetido 4 vezes com 2 segundos de espera entre cada repetição
for _ in range(5):
    pyautogui.press('enter')  # Pressiona Enter
    time.sleep(5)  # Aguarda 2 segundos antes de repetir

# Passo 4: Abri janela de relatórios
pyautogui.hotkey('ctrl', 'r')
time.sleep(10)

# abre o relatório favorito de preços
pyautogui.click(x=120, y=600)
time.sleep(5)

# Clica no grupo inicial
pyautogui.click(x=578, y=245)
pyautogui.write('005')
time.sleep(2)

# Clica no grupo final
pyautogui.doubleClick(x=918, y=246)
time.sleep(1)
pyautogui.write('020')
time.sleep(4)

# Na aba Quantidades, clica em valor de vendas 1
pyautogui.click(x=434, y=532)
time.sleep(4)

# Clica em preview
pyautogui.click(x=754, y=780)
time.sleep(25)

# Clica em salvar
pyautogui.click(x=702, y=49)
time.sleep(15)

# escrever nome arquivo e tipo arquivo
pyautogui.write('produtos_expert.XLS')
pyautogui.press('tab')
time.sleep(4)
pyautogui.click(x=1233, y=695)
pyautogui.write('e')
pyautogui.press('tab')
pyautogui.press('enter')
time.sleep(10)
