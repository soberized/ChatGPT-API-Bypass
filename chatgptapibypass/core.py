# chatgpt_automator/core.py

import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
import signal
import random 

def chatgpt(prompt: str, search: bool = False) -> str | None:
    """
    Launches an undetected Chrome browser, navigates to ChatGPT.com,
    enters the provided prompt, submits it, waits for the response,
    and returns the assistant's response text.

    Args:
        prompt (str): The text prompt to send to ChatGPT.
        search (bool): If True, attempts to enable the search mode button
                       (if available on the ChatGPT interface). Defaults to False.

    Returns:
        str | None: The assistant's response text if successful, None otherwise.
    """
    driver = None
    try:
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.2535.85",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
        ]
        
      
        selected_user_agent = random.choice(user_agents)

       
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080') 
        options.add_argument('--disable-blink-features=AutomationControlled') # Evade detection
        options.add_argument(f'user-agent={selected_user_agent}') # user agent
        
      
        options.add_argument('--start-maximized') # maximum window size
        options.add_argument('--disable-infobars') # infobars
        options.add_argument('--disable-extensions') # extensions
        options.add_argument('--no-zygote') # zygote process for more isolation
        options.add_argument('--disable-setuid-sandbox') 
        options.add_argument('--disable-web-security') # cross-origin issues
        
      
        time.sleep(0.5)

      
        driver = uc.Chrome(options=options)
        
        
        driver.get("https://chatgpt.com/?model=auto")
        print("Successfully launched ChatGPT.com with undetected Chrome in headless mode.")
        
        # Wait for the page to be fully loaded
        print("Waiting for page to fully load (document.readyState == 'complete')...")
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("Page fully loaded.")
        
       

        print("Waiting for input field (ProseMirror) to be present, visible, and ready...")
        
       
        input_container = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ProseMirror[contenteditable="true"]'))
        )
        print("ProseMirror container found and visible.")

      
        input_field = None
        try:
            input_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.ProseMirror[contenteditable="true"] p[data-placeholder*="Ask anything"], div.ProseMirror[contenteditable="true"] p.placeholder, div.ProseMirror[contenteditable="true"]'))
            )
            print("Specific input field element within ProseMirror found.")
        except TimeoutException:
            print("Specific input field element not found within ProseMirror, defaulting to ProseMirror container.")
            input_field = input_container #  <p> isn't found

      
        print("Scrolling input field into view and waiting for it to be clickable...")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        time.sleep(0.5) 
        
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(input_field) 
        )
        print("Input field is clickable.")

       
        driver.execute_script("arguments[0].click();", input_field)
        driver.execute_script("arguments[0].focus();", input_field)
        time.sleep(0.5) 
        
      
        driver.execute_script("arguments[0].innerHTML = '';", input_field)
        
        
        escaped_prompt = prompt.replace("'", "\\'").replace('\n', '\\n').replace('"', '\\"') 
        driver.execute_script(f"arguments[0].innerHTML = '{escaped_prompt}';", input_field)
        
      
        driver.execute_script("""
            const event = new Event('input', { bubbles: true });
            arguments[0].dispatchEvent(event);
        """, input_field)
        
        print(f"Successfully entered prompt: '{prompt[:50]}...'")

        if search:
            print("Attempting to enable search mode...")
            try:
                search_button_selector = 'button[data-testid*="composer-button-"], button:has(span[data-localize="composer.web-access.title"]), button:has(div[class*="icon"] > svg[aria-label*="search"]), button:has(div:text-i("search"))'
                search_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, search_button_selector))
                )
                driver.execute_script("arguments[0].click();", search_button)
                print("Search mode button clicked (if available).")
            except TimeoutException:
                print("Search button not found or not clickable within timeout. Proceeding without search.")
            except Exception as e:
                print(f"Error clicking search button: {e}. Proceeding without search.")

        
        print("Waiting for send button to be clickable...")
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Send message"], button[data-testid="send-button"]'))
        )
        print("Send button found. Clicking it using JavaScript...")
        driver.execute_script("arguments[0].click();", send_button)
        print("Prompt submitted by clicking the send button.")
        
        
        print("Waiting for response to start streaming (stop button to appear)...")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Stop generating"], button[data-testid="stop-button"]'))
        )
        print("Response streaming detected. Waiting for response to complete (stop button to disappear)...")
        
        
        WebDriverWait(driver, 180).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Stop generating"], button[data-testid="stop-button"]'))
        )
        print("Response generation completed.")
        
        
        print("Attempting to extract assistant's response...")
        response_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-message-author-role="assistant"]'))
        )
        
        if response_elements:
            response_element = response_elements[-1] 
            response_text = response_element.text
            print("Successfully extracted response text.")
            return response_text
        else:
            print("No assistant response elements found after completion.")
            return None
            
    except Exception as e:
        print(f"An error occurred during ChatGPT interaction: {e}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
                print("Browser closed gracefully.")
            except Exception as quit_e:
                print(f"Error during graceful quit: {quit_e}. Attempting forceful cleanup.")
                try:
                    if hasattr(driver, 'service') and driver.service and driver.service.process:
                        pid = driver.service.process.pid
                        if pid:
                            if os.name == 'nt':  # Windows
                                os.system(f'taskkill /F /T /PID {pid}')
                            else:  # Unix-like systems
                                os.kill(pid, signal.SIGTERM)
                            print(f"Forcefully terminated process with PID: {pid}")
                except Exception as force_e:
                    print(f"Error during forceful cleanup: {force_e}. Some browser processes might remain.")

