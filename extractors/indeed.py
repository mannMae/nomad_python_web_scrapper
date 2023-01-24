from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page_count(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)

    browser.get(f"https://www.indeed.com/jobs?q={keyword}&limit=50")

    print(13, browser.page_source)

    result = []

    soup = BeautifulSoup(browser.page_source, "html.parser")

    pagination = soup.find("ul", class_="pagination-list")
    if pagination == None:
        return 1
    pages = pagination.find_all("li", recursive=False)
    count = len(pages)
    if count >=5:
        return 5
    return count

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    result = []
    for page in range(pages):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        browser = webdriver.Chrome(options=options)
        
        base_url = "https://www.indeed.com/jobs"
        url = f"{base_url}?q={keyword}&start={page * 10}"

        browser.get(url)

        print(13, browser.page_source)


        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                print(anchor)
                title = anchor["aria-label"]
                link = anchor["href"]
                
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    "link" : f"https://kr.indeed.com{link}",
                    "company" : company.string.replace(",", " "),
                    "location" : location.string.replace(",", " "),
                    "position" : title.replace(",", " ")
                }
                result.append(job_data)
                

    print(result)
    return result