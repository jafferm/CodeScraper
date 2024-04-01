from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def contract_checker1(model_code):
    print("running contract code")
    # Execute the code snippet to create the model
    exec(model_code)
    
    # Assuming the model variable is defined after executing the code
    concatenate_layers = [layer for layer in model.layers if isinstance(layer, Concatenate)]

    for concatenate_layer in concatenate_layers:
        if concatenate_layer.input_shape is None or None in concatenate_layer.input_shape:
            print("Input shape not specified for a Concatenate layer.")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://github.com/login")

# Fill in the login credentials and submit the form
username_input = driver.find_element(By.ID, "login_field")
password_input = driver.find_element(By.ID, "password")
submit_button = driver.find_element(By.NAME, "commit")

username_input.send_keys("username")#give your github username
password_input.send_keys("password")#give your github password
submit_button.click()

# Wait for the search page to load
button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-target='qbsearch-input.inputButton']"))
)

# Click on the button
button.click()


search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "query-builder-test"))
)

# Input text into the search field
search_input.send_keys("keras.layers.concatenate"+ Keys.ENTER)

# Wait for the button to be clickable to move from repository to code
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, ":r3:--label"))
)

# Click on the button
button.click()

links = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[@data-testid='link-to-search-result']"))
)

# Extract href attributes from all links
link_urls = [link.get_attribute('href') for link in links]

# Now you have all the URLs
print(len(link_urls))
tot = 0
for link in link_urls:
    driver.get(link)
    try:
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@data-testid='read-only-cursor-text-area']"))
        )

        # Get the text content of the textarea
        code_content = textarea.text
        if 'keras.layers.concatenate' in code_content:
            tot += 1
    except Exception as e:
        print("Exception occurred:", e)

print("total number: " +str(tot))




# Wait for the link to be clickable
# link = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='link-to-search-result']"))
# )
# # Click on the link
# link.click()

# textarea = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//textarea[@data-testid='read-only-cursor-text-area']"))
# )

# # Get the text content of the textarea
# code_content = textarea.text

# print(code_content)
# #exec(code_content)
# #contract_checker1(code_content)
# # Wait for a while (optional)
time.sleep(120)

# Quit the browser
driver.quit()
