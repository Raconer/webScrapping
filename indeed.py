import requests
from bs4 import BeautifulSoup

LIMIT = 50
# URL =f"https://kr.indeed.com/jobs?q=python&l=인천&limit={LIMIT}"
URL =f"https://indeed.com/jobs?q=python&limit={LIMIT}"
APPLY_URL = "https://www.indeed.com/viewjob?jk="

def get_last_page():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, 'html.parser')

  pagination = soup.find("div", {
    "class": "pagination"
  })

  links = pagination.find_all('a')

  spans = []

  for link in links[:-1]:
    spans.append(int(link.string))

  return spans[-1]

def extract_job(html):
  # Find Title
  title = html.find("h2", {"class": "title"})
  if title:
    title_anchor = title.find("a")
    if title_anchor is not None:
     title = str(title_anchor["title"])
    else:
      title = str(title.string)
  else:
    title = None
  # Find Company
  company = html.find("span", {"class": "company"})
  if company:
    company_anchor = company.find("a")
    if company_anchor is not None:
      company = str(company_anchor.string)
    else:
      company = str(company.string)
  else:
    company = None  
  company = company.strip()
  # Find Location
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  # job_id
  job_id = html["data-jk"]

  return {"title" : title, "company": company, "location": location, "link" : APPLY_URL+job_id}

def extract_jobs(last_pages):
  jobs = []
  for page in range(last_pages):
    print(f"Scrapping Indeed: Page: {page}")
    result = requests.get(f"{URL}&start={0*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class" : "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(2)
  return jobs