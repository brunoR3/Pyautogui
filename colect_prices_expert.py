import pyautogui
import time
import os
import logging
import sys
from datetime import datetime

# Configure logging
log_filename = f"price_collection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout)
    ]
)

# Caminho do ERP
erp_path = r'C:\Atx\AtxExec.exe'

def safe_click(x, y, description=""):
    """Safely perform a mouse click with error handling"""
    try:
        logging.info(f"Clicking at position ({x}, {y}): {description}")
        pyautogui.click(x=x, y=y)
        return True
    except Exception as e:
        logging.error(f"Failed to click at position ({x}, {y}): {e}")
        return False

def safe_double_click(x, y, description=""):
    """Safely perform a mouse double click with error handling"""
    try:
        logging.info(f"Double-clicking at position ({x}, {y}): {description}")
        pyautogui.doubleClick(x=x, y=y)
        return True
    except Exception as e:
        logging.error(f"Failed to double-click at position ({x}, {y}): {e}")
        return False

def safe_write(text, description=""):
    """Safely type text with error handling"""
    try:
        logging.info(f"Writing text: '{text}' ({description})")
        pyautogui.write(text)
        return True
    except Exception as e:
        logging.error(f"Failed to write text '{text}': {e}")
        return False

def safe_keypress(key, description=""):
    """Safely press a key with error handling"""
    try:
        logging.info(f"Pressing key: {key} ({description})")
        pyautogui.press(key)
        return True
    except Exception as e:
        logging.error(f"Failed to press key '{key}': {e}")
        return False

def safe_hotkey(key1, key2, description=""):
    """Safely press a hotkey combination with error handling"""
    try:
        logging.info(f"Pressing hotkey: {key1}+{key2} ({description})")
        pyautogui.hotkey(key1, key2)
        return True
    except Exception as e:
        logging.error(f"Failed to press hotkey '{key1}+{key2}': {e}")
        return False

def open_erp():
    """Open the ERP application"""
    try:
        logging.info(f"Opening ERP application: {erp_path}")
        os.startfile(erp_path)
        time.sleep(10)  # Wait for ERP to load
        return True
    except FileNotFoundError:
        logging.error(f"ERP executable not found at path: {erp_path}")
        return False
    except Exception as e:
        logging.error(f"Failed to open ERP application: {e}")
        return False

def login_to_erp():
    """Login to the ERP system"""
    try:
        logging.info("Starting login process")
        
        # Click login field and enter username
        if not safe_click(808, 588, "login field"):
            return False
        if not safe_write('user', "username"):
            return False
        time.sleep(5)
        
        # Click password field and enter password
        if not safe_click(809, 634, "password field"):
            return False
        if not safe_write('senha', "password"):
            return False
        time.sleep(5)
        
        # Press Enter multiple times to complete login
        logging.info("Pressing Enter multiple times to complete login")
        for i in range(5):
            if not safe_keypress('enter', f"login attempt {i+1}"):
                return False
            time.sleep(5)
            
        logging.info("Login completed successfully")
        return True
    except Exception as e:
        logging.error(f"Error during login process: {e}")
        return False

def open_reports():
    """Open the reports window"""
    try:
        logging.info("Opening reports window")
        if not safe_hotkey('ctrl', 'r', "open reports window"):
            return False
        time.sleep(10)
        
        # Open favorite price report
        if not safe_click(120, 600, "favorite price report"):
            return False
        time.sleep(5)
        
        logging.info("Reports window opened successfully")
        return True
    except Exception as e:
        logging.error(f"Error opening reports: {e}")
        return False

def set_report_parameters():
    """Set parameters for the report"""
    try:
        logging.info("Setting report parameters")
        
        # Set initial group
        if not safe_click(578, 245, "initial group field"):
            return False
        if not safe_write('005', "initial group value"):
            return False
        time.sleep(2)
        
        # Set final group
        if not safe_double_click(918, 246, "final group field"):
            return False
        time.sleep(1)
        if not safe_write('020', "final group value"):
            return False
        time.sleep(4)
        
        # Click on "Quantities" tab, sales value 1
        if not safe_click(434, 532, "sales value 1 option"):
            return False
        time.sleep(4)
        
        logging.info("Report parameters set successfully")
        return True
    except Exception as e:
        logging.error(f"Error setting report parameters: {e}")
        return False

def generate_and_save_report():
    """Generate the report and save it to file"""
    try:
        logging.info("Generating report preview")
        
        # Click preview button
        if not safe_click(754, 780, "preview button"):
            return False
        time.sleep(25)  # Wait for report generation
        
        # Click save button
        logging.info("Saving report to file")
        if not safe_click(702, 49, "save button"):
            return False
        time.sleep(15)
        
        # Enter filename and file type
        if not safe_write('produtos_expert.XLS', "filename"):
            return False
        if not safe_keypress('tab', "move to file type"):
            return False
        time.sleep(4)
        
        if not safe_click(1233, 695, "file type dropdown"):
            return False
        if not safe_write('e', "select Excel format"):
            return False
        if not safe_keypress('tab', "confirm file type"):
            return False
        if not safe_keypress('enter', "save file"):
            return False
        
        time.sleep(10)
        logging.info("Report saved successfully as 'produtos_expert.XLS'")
        return True
    except Exception as e:
        logging.error(f"Error generating or saving report: {e}")
        return False

def main():
    """Main function to run the price collection process"""
    try:
        logging.info("Starting price collection process")
        
        # Step 1: Open ERP
        if not open_erp():
            logging.error("Failed to open ERP application. Exiting.")
            return False
        
        # Step 2: Login to ERP
        if not login_to_erp():
            logging.error("Failed to login to ERP. Exiting.")
            return False
        
        # Step 3: Open reports window
        if not open_reports():
            logging.error("Failed to open reports window. Exiting.")
            return False
        
        # Step 4: Set report parameters
        if not set_report_parameters():
            logging.error("Failed to set report parameters. Exiting.")
            return False
        
        # Step 5: Generate and save report
        if not generate_and_save_report():
            logging.error("Failed to generate and save report. Exiting.")
            return False
        
        logging.info("Price collection process completed successfully")
        return True
    except pyautogui.FailSafeException:
        logging.critical("PyAutoGUI failsafe triggered - mouse moved to corner of screen. Process aborted.")
        return False
    except Exception as e:
        logging.critical(f"Unexpected error in main process: {e}")
        return False

# Execute the main function if script is run directly
if __name__ == "__main__":
    try:
        # Set PyAutoGUI failsafe
        pyautogui.FAILSAFE = True
        logging.info("PyAutoGUI failsafe enabled - move mouse to corner of screen to abort")
        
        # Run the main process
        result = main()
        
        # Log final status
        if result:
            logging.info("Script executed successfully")
        else:
            logging.warning("Script execution completed with errors")
            
    except KeyboardInterrupt:
        logging.warning("Script interrupted by user")
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
    finally:
        logging.info("Script execution finished")
