import requests
from bs4 import BeautifulSoup

URL = f"http://stackoverflow.com/jobs?q=python&sort=y"

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class" : "s-pagination"}).find_all("a")
  # return int(pages[-2].get_text(strip=True))
  return 2

def extract_job(html):
  title = html.find("div", {"class":"grid--cell fl1"}).find("h2").find("a")["title"]
  company, location = html.find("h3", {"class":"fc-black-700"}).find_all("span", recursive=False)# recursive=False : 첫째 단계의 span만 가져온다.
  # Get Company
  company = company.get_text(strip=True)
  # Get Location
  location = location.get_text(strip=True).strip("-").strip("\n").strip("\r")
  # Get Job Id
  job_id = html['data-jobid']
  return {'title': title, 'company' : company, 'location' : location, 'apply_link': f"https://stackoverflow.com/jobs/{job_id}"}
  
def extract_jobs(last_page):
  jobs = []
  
  for page in range(last_page):
    print(f"Scrapping SO: Page : {page}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text,"html.parser")
    results = soup.find_all("div", {"class":"-job"})

    for result in results:
      job = extract_job(result)
      jobs.append(job)

 
  return jobs


def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  
  return jobs