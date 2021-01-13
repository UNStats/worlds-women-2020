from selenium import webdriver


driver = webdriver.Chrome('C:/Users/LGONZALE20/Downloads/chromedriver.exe')
driver.get('https://unstats.un.org/unsd/demographic-social/gender/worldswomen/2020/power-nd1-graph-2')
driver.execute_script('document.body.style.zoom = "85%"')
screenshot = driver.save_screenshot('my_screenshot.png')
driver.quit()

