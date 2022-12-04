from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By 
from pathlib import Path
import unittest

class WCResultsScrapper(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="web_scrapping\chromedriver.exe")
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.get("https://onefootball.com/en/competition/fifa-world-cup-12/fixtures")

    def test_get_scores(self):
        cookies_btn = self.driver.find_element(By.CSS_SELECTOR,"#onetrust-accept-btn-handler")
        self.driver.implicitly_wait(5)
        self.assertTrue(cookies_btn.is_displayed())
        cookies_btn.click()
        
        expand_btn_css = ".match-cards-lists-appender__load-all-button-container:has(span.of-button__content)"
        while(self.is_element_present(By.CSS_SELECTOR,expand_btn_css)):
            expand_btn = self.driver.find_element(By.CSS_SELECTOR,expand_btn_css)
            self.assertTrue(expand_btn.is_enabled())
            self.driver.implicitly_wait(5)
            ActionChains(self.driver).move_to_element(expand_btn).click(expand_btn).perform()
        
        self.currentResults = self.driver.page_source

    def tearDown(self):
        self.driver.quit()
        if self.currentResults:
            with open(Path(Path(__file__).parent,"WCresults.html"),"w",encoding="utf-8") as f:
                f.write(self.currentResults)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as variable:
            return False
        return True

if __name__ == "__main__":
    unittest.main(verbosity=2)