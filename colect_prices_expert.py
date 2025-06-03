import pyautogui
import time
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('price_collector')

# Path for storing reference images
REF_IMAGES_DIR = Path('reference_images')

# Create reference images directory if it doesn't exist
REF_IMAGES_DIR.mkdir(exist_ok=True)

# Caminho do ERP
erp_path = r'C:\Atx\AtxExec.exe'

# Função para criar screenshots de referência (usado apenas durante a configuração inicial)
def capture_reference_images():
    """Capture reference images for UI elements.
    
    This function should be run once to create the reference images,
    then commented out in normal operation.
    """
    input("Press Enter when ERP is open and login screen is visible...")
    pyautogui.screenshot(str(REF_IMAGES_DIR / 'login_field.png')).save(str(REF_IMAGES_DIR / 'login_field.png'))
    input("Now click on the password field and press Enter...")
    pyautogui.screenshot(str(REF_IMAGES_DIR / 'password_field.png')).save(str(REF_IMAGES_DIR / 'password_field.png'))
    # Continue for other UI elements...
    logger.info("Reference images captured. You can now comment out this function call.")

# Descomentar a linha abaixo apenas na primeira execução para capturar imagens de referência
# capture_reference_images()

# Função para localizar uma imagem na tela e clicar nela
def click_on_image(image_name, confidence=0.7, timeout=10, offset_x=0, offset_y=0):
    """Finds an image on screen and clicks on it with optional offset.
    
    Args:
        image_name: Name of the reference image file (must be in REF_IMAGES_DIR)
        confidence: Match confidence threshold (0-1)
        timeout: Maximum time to wait for image (seconds)
        offset_x: X-offset from center of found image
        offset_y: Y-offset from center of found image
    
    Returns:
        True if successful, False otherwise
    """
    image_path = REF_IMAGES_DIR / image_name
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center_x, center_y = pyautogui.center(location)
                pyautogui.click(center_x + offset_x, center_y + offset_y)
                logger.info(f"Clicked on {image_name}")
                return True
        except (pyautogui.ImageNotFoundException, OSError) as e:
            logger.warning(f"Image {image_name} not found: {e}")
        
        logger.debug(f"Waiting for {image_name} to appear...")
        time.sleep(0.5)
    
    logger.error(f"Timed out waiting for {image_name}")
    return False

# Fallback function to use hard-coded coordinates when image recognition fails
def fallback_click(x, y, description):
    """Fallback to clicking at specific coordinates when image recognition fails.
    
    Args:
        x: X-coordinate
        y: Y-coordinate
        description: Description of the UI element for logging
    """
    logger.warning(f"Using fallback for {description} at coordinates ({x}, {y})")
    pyautogui.click(x, y)

# Passo 1: Abrir o ERP
logger.info(f"Starting ERP application from {erp_path}")
try:
    os.startfile(erp_path)
    logger.info("ERP application started successfully")
except Exception as e:
    logger.error(f"Failed to start ERP application: {e}")
    sys.exit(1)

# Aguardar alguns segundos para garantir que o ERP carregue
logger.info("Waiting for ERP to load...")
time.sleep(10)

# Passo 2: Fazer login no sistema
# Tentar clicar no campo de login usando reconhecimento de imagem
login_successful = False

# Tenta localizar o campo de login pela imagem
if click_on_image('login_field.png', timeout=5):
    pyautogui.write('user')
    time.sleep(1)
    
    # Tenta localizar o campo de senha pela imagem
    if click_on_image('password_field.png', timeout=5):
        pyautogui.write('senha')
        login_successful = True
else:
    # Fallback para coordenadas fixas caso a detecção de imagem falhe
    logger.warning("Falling back to hardcoded coordinates for login fields")
    # Campo de login
    fallback_click(808, 588, "login field")
    pyautogui.write('user')
    time.sleep(1)
    
    # Campo de senha
    fallback_click(809, 634, "password field")
    pyautogui.write('senha')

# Passo 3: Pressionar Enter para fazer login repetido 5 vezes com espera entre cada repetição
for i in range(5):
    logger.info(f"Pressing Enter (attempt {i+1}/5)")
    pyautogui.press('enter')
    time.sleep(5)

# Passo 4: Abrir janela de relatórios
logger.info("Opening reports window with Ctrl+R")
pyautogui.hotkey('ctrl', 'r')
time.sleep(10)

# Tenta localizar e clicar no relatório favorito de preços
if not click_on_image('favorite_report.png', timeout=5):
    # Fallback para coordenadas fixas
    fallback_click(120, 600, "favorite report")
time.sleep(5)

# Tenta clicar no campo de grupo inicial usando reconhecimento de imagem
if not click_on_image('initial_group_field.png', timeout=5):
    # Fallback para coordenadas fixas
    fallback_click(578, 245, "initial group field")
pyautogui.write('005')
time.sleep(2)

# Tenta clicar no campo de grupo final usando reconhecimento de imagem
if not click_on_image('final_group_field.png', timeout=5):
    # Fallback para coordenadas fixas
    fallback_click(918, 246, "final group field")
    pyautogui.doubleClick()
time.sleep(1)
pyautogui.write('020')
time.sleep(4)

# Tenta clicar na aba Quantidades, valor de vendas 1
if not click_on_image('sales_value_field.png', timeout=5):
    # Fallback para coordenadas fixas
    fallback_click(434, 532, "sales value field")
time.sleep(4)

# Tenta clicar no botão de preview
if not click_on_image('preview_button.png', timeout=5):
    # Fallback para coordenadas fixas
    fallback_click(754, 780, "preview button")
time.sleep(25)  # Aguarda o relatório carregar

# Tenta clicar no botão de salvar
if not click_on_image('save_button.png', timeout=5):
    # Fallback para coordenadas fixas
    fallback_click(702, 49, "save button")
time.sleep(15)  # Aguarda o diálogo de salvar abrir

# Escreve o nome do arquivo e escolhe o tipo
pyautogui.write('produtos_expert.XLS')
pyautogui.press('tab')
time.sleep(4)

# Tenta clicar no campo de tipo de arquivo
if not click_on_image('file_type_field.png', timeout=5):
    # Fallback para coordenadas fixas
    fallback_click(1233, 695, "file type field")
pyautogui.write('e')  # Seleciona Excel
pyautogui.press('tab')
pyautogui.press('enter')
time.sleep(10)

logger.info("Price collection completed successfully!")