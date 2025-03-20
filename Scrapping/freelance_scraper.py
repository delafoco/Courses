from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import json
from datetime import datetime
import os
from dotenv import load_dotenv

class FreelanceScraper:
    def __init__(self):
        load_dotenv()  # Charge les variables d'environnement
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')  # Mode sans interface graphique
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=self.options)
        self.results = []

    def login_linkedin(self):
        """Connexion à LinkedIn"""
        print("Connexion à LinkedIn...")
        self.driver.get("https://www.linkedin.com/login")
        time.sleep(3)

        # Récupération des identifiants depuis les variables d'environnement
        email = os.getenv('LINKEDIN_EMAIL')
        password = os.getenv('LINKEDIN_PASSWORD')

        if not email or not password:
            print("Erreur: Identifiants LinkedIn non trouvés dans le fichier .env")
            return False

        try:
            # Remplissage du formulaire de connexion
            self.driver.find_element(By.ID, "username").send_keys(email)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            time.sleep(5)
            return True
        except Exception as e:
            print(f"Erreur lors de la connexion à LinkedIn: {str(e)}")
            return False

    def scrape_malt(self):
        """Scrape les annonces de Malt.fr"""
        print("Scraping Malt.fr...")
        self.driver.get("https://www.malt.fr/search?q=power%20bi%20data%20science")
        time.sleep(5)  # Attente du chargement

        try:
            # Attendre que les annonces se chargent
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "freelance-card"))
            )

            # Récupérer les annonces
            annonces = self.driver.find_elements(By.CLASS_NAME, "freelance-card")
            
            for annonce in annonces:
                try:
                    titre = annonce.find_element(By.CLASS_NAME, "freelance-card__title").text
                    url = annonce.find_element(By.TAG_NAME, "a").get_attribute("href")
                    self.results.append({
                        "site": "Malt",
                        "titre": titre,
                        "url": url,
                        "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except:
                    continue

        except TimeoutException:
            print("Timeout lors du chargement de Malt.fr")

    def scrape_freelance_info(self):
        """Scrape les annonces de Freelance-info.com"""
        print("Scraping Freelance-info.com...")
        self.driver.get("https://www.freelance-info.fr/recherche?q=power+bi+data+science")
        time.sleep(5)

        try:
            # Attendre que les annonces se chargent
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mission-card"))
            )

            # Récupérer les annonces
            annonces = self.driver.find_elements(By.CLASS_NAME, "mission-card")
            
            for annonce in annonces:
                try:
                    titre = annonce.find_element(By.CLASS_NAME, "mission-card__title").text
                    url = annonce.find_element(By.TAG_NAME, "a").get_attribute("href")
                    self.results.append({
                        "site": "Freelance-info",
                        "titre": titre,
                        "url": url,
                        "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except:
                    continue

        except TimeoutException:
            print("Timeout lors du chargement de Freelance-info.com")

    def scrape_linkedin(self):
        """Scrape les annonces de LinkedIn"""
        if not self.login_linkedin():
            return

        print("Scraping LinkedIn...")
        self.driver.get("https://www.linkedin.com/jobs/search/?keywords=power%20bi%20data%20science&f_AL=true&f_WT=2")
        time.sleep(5)

        try:
            # Attendre que les annonces se chargent
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "job-card-container"))
            )

            # Récupérer les annonces
            annonces = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
            
            for annonce in annonces:
                try:
                    titre = annonce.find_element(By.CLASS_NAME, "job-card-list__title").text
                    url = annonce.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
                    self.results.append({
                        "site": "LinkedIn",
                        "titre": titre,
                        "url": url,
                        "date_scraping": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except:
                    continue

        except TimeoutException:
            print("Timeout lors du chargement de LinkedIn")

    def save_results(self):
        """Sauvegarde les résultats dans un fichier CSV et JSON"""
        # Sauvegarde en CSV
        df = pd.DataFrame(self.results)
        df.to_csv(f"freelance_missions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)
        
        # Sauvegarde en JSON
        with open(f"freelance_missions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)

    def close(self):
        """Ferme le navigateur"""
        self.driver.quit()

def main():
    # Création d'une instance de la classe FreelanceScraper pour scraper les offres d'emploi
    scraper = FreelanceScraper()
    try:
        
        scraper.scrape_linkedin()  # Ajout du scraping LinkedIn
        scraper.save_results()
        print(f"\nNombre total d'annonces trouvées : {len(scraper.results)}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main() 