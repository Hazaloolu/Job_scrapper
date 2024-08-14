import requests
from bs4 import BeautifulSoup
from notion_client import Client

URL = "https://realpython.github.io/fake-jobs/"

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="ResultsContainer")


python_jobs = results.find_all("h2", string=lambda text: "python" in text.lower())

python_job_elements = [h2_element.parent.parent.parent for h2_element in python_jobs]


# Notion Setup



notion = Client(auth=NOTION_API_KEY)


# ADD JOB TO NOTION

def add_job_to_notion(title, company,location,apply_link) :
    notion.pages.create(
        parent={'database_id': DATABASE_ID},
        properties = {
            "Title": {"title": [{"text": {"content": title}}]},
            "Company": {"rich_text": [{"text": {"content": company}}]},
            "Location": {"rich_text": [{"text": {"content": location}}]},
            "Apply Link": {"url": apply_link}
            
        }

    )




# process each job and add to notion

for job_element in python_job_elements:
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")

    link_url = job_element.find_all("a")[1]["href"]

    title = title_element.text.strip()
    company = company_element.text.strip()
    location = location_element.text.strip()

    add_job_to_notion(title, company, location, link_url)
    print(f"Added job: {title}")


print("All jobs have been added to notion")
    



