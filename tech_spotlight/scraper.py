import requests
import urllib
from bs4 import BeautifulSoup
import time
import random
import sys
from . import tech_term_search


"""
Global
TODO: typehint menthods/function
TODO: add inline comments for vauge code or refactor for readability
TODO: impliment mock with testing for scraper.py
DONE: impliment pre-commit / commitizen.
DONE: rename function/methods for readability
DONE: refactor control flow prints as variables to call within application flow.
"""

# all strings here are used within Main function
welcome_str = """
        >>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<
        >>>>>>>>>>> Welcome to the Tech Spotlight <<<<<<<<<<
        >>> This tool, scrapes indeed for a given search <<<
        >>> query, returning both a raw text file, and   <<<
        >>> a processed .CSV file, containing the number <<<
        >>> of times a given term appears in the raw     <<<
        >>> text.                                        <<<
        >>>                                              <<<
        >>> If you would like to see the technologies we <<<
        >>> are counting, the list is under /datasets as <<<
        >>> tech_list.txt                                <<<
        >>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<
    """
search_query_str = """
    > Please enter a development job title to search for,
    i.e. 'software developer', 'software engineer',
    'dev ops engineer' etc.
    > """
location_query_str = """
    > Please enter a location to search, i.e. 'remote',
    'seattle', 'chicago' etc.
    > """
age_query_str = """
    > Please enter a job post age to scrape, accepted inputs
    are as follows:
    '1' for postings within the last 24 hours
    '3' for postings within the last 3 days
    '5' for postings within the last 5 days
    '7' for postings within the last 7 days
    > """
scrape_num_query_str = """
    > Please enter a number of jobs to scrape,
    this determines the size of the dataset,
    keep in mind the larger the dataset the longer
    the scrape will take.

    example: a scrape of 900 jobs will take
    over an hour in most cases, and runs the risk
    of being stopped by indeed. Consider using a
    VPN if scraping more than 300 jobs.
    ---> The scraper will pause for a number of
    minutes every 100 jobs. <---

    Please enter a number of jobs to scrape > """
file_query_str = """
    > Please enter output filename, raw file
    will be a .txt file
    !! You do not need to add the .txt extension !!
    example input: dev_ops_Seattle_300_jobs
    example output: dev_ops_Seattle_300_jobs.txt
    > """


def format_url(job_title, location, age, start):
    """
    Function receives args and formats URL query for each cycle through scraper.
    :param job_title: string
    :param location: string
    :param age: int
    :param start: int default 0, increments by 10 each iteration of scraper function
    :return: complete formatted url
    """
    get_vars = {"q": job_title, "l": location, "fromage": age, "start": start}
    url = "https://www.indeed.com/jobs?" + urllib.parse.urlencode(get_vars)
    print("your search URL: " + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_="jobsearch-ResultsList")
    return results


def get_input():
    """
    Function called during scrape execution, this forces a
    pause to get user input, Helping to avoid rate limit.
    Asks if user wants to continue or stop the scrape.
    :return: None
    """
    print(">> Consider swapping IP address with a VPN to avoid rate limit. <<")
    input_ = input(">> 'c' to continue your scrape, 'q' to quit here <<")
    input_ = input_.lower()
    print(input_)
    if input_ == "c":
        print(">> Continuing scrape <<")
        return
    elif input_ == "q":
        print(">> are you sure you want to stop the scrape? <<")
        confirm = input(">> 'quit' to quit scraping, 'c' to continue << ")
        print(confirm)
        confirm = confirm.lower()
        if confirm == "c":
            print(">> Continuing scrape <<")
            return
        elif confirm == "quit":
            sys.exit()
        else:
            print(">> unexpected input received <<")
            get_input()
    else:
        print(">> unexpected input received <<")
        get_input()


def main():
    """
    prompts user for search params and calls scraper.
    :return: N/A Calls scraper
    """
    age_inputs = ["1", "3", "5", "7"]

    # Welcome user, and prompt for scrape query params
    print(welcome_str)
    job_tile = input(search_query_str)
    location = input(location_query_str)
    age = input(age_query_str)
    # continue prompting for correct age input
    while age not in age_inputs:
        print(">>> Invalid post age received <<<")
        age = input(age_query_str)
    scrapes = input(scrape_num_query_str)
    filename = input(file_query_str)

    # all needed inputs received, begin scrape
    print(
        f"""
    Beginning scrape of Indeed.com for the following query
    job tile: {job_tile}
    location: {location}
    age: {age}
    scrapes: {scrapes}
    filename: {filename}
    After scraper is done the raw txt file will
    be processed into a csv file.

    Your raw text file will be called: {filename}.txt
    Your processed csv file will be called: {filename}_terms.csv

    Your scrape will begin shortly...
    """
    )
    time.sleep(2)
    # call scraper with provided user inputs
    scraper(job_tile, location, age, int(scrapes), filename)
    raw_file_path = f"{filename}.txt"
    csv_file_path = f"{filename}_terms.csv"
    tech_term_search.write_data(
        (
            "/Users/bencarter/projects/Code401/"
            f"tech-spotlight/tech_spotlight/{raw_file_path}"
        ),
        "/Users/bencarter/projects/Code401/tech-spotlight/datasets/tech_list.txt",
        csv_file_path,
    )
    print(
        f"""
    Tech Spotlight has finished the scrape and
    processed the raw data into a csv file.
    The csv file name is : {filename}_terms.csv
    We encourage you to fork this notebook and
    import your new dataset to visualize your data.
    https://www.kaggle.com/code/edenbrekke/tech-spotlight-indeed-web-scraper-template/notebook
    """
    )


def scraper(job_title: str, location: str, age: int, scrapes: int, filename: str):
    """
    Main application function, calls all other functions to perform the
    requested job scrape.

    :param job_title: Job title, such as "software engineer", "python developer"
    :type job_title: str
    :param location: Location name, such as "seattle" "remote" "chicago"
    :type location: str
    :param age: 1 3 5 or 7
    :type age: int
    :param scrapes: "50" to scrape 50 job posts
    :type scrapes: int
    :param filename: string
    :return: raw text file
    """
    start = 0
    scrapes = scrapes
    scraped_jobs = 0
    job_id_set = set()
    break_time = 0
    while scraped_jobs < int(scrapes):
        results = format_url(job_title, location, age, start)

        if results is None:
            print(
                f"""
                    >>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<
                    >>> Nonetype received, you likely hit a captcha <<<
                    >>> or ran out of job posts for a given search, <<<
                    >>> unfortunately scraper cannot recover from   <<<
                    >>> this. You will need to start over. Try,     <<<
                    >>> using a vpn, to swap your IP address mid    <<<
                    >>> scrape.                                     <<<
                        We successfully scraped {scraped_jobs}
                        out of the attempted {scrapes} total.
                    >>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<
                """
            )
            sys.exit()

        for element in results:
            a_tag = element.find("a")

            if break_time == 100:
                break_time = 0
                wait_time = random.randint(240, 360)
                print(f"waiting for {wait_time} this long (seconds)")
                time.sleep(wait_time)

            if scraped_jobs == 350 or scraped_jobs == 700:
                get_input()

            if a_tag:
                job_id = a_tag.get("data-jk")
                if job_id in job_id_set:
                    continue

                else:
                    job_id_set.add(job_id)
                    scraped_jobs = len(job_id_set)
                    break_time += 1

                    description = job_id_to_description(job_id)
                    file = str(filename) + ".txt"
                    with open(file, "a+", encoding="utf-8") as f:
                        f.write(description)
                        f.write(
                            "\n \n _________________________________"
                            "New Job______________________________ \n \n "
                        )
                    print(str(job_id) + " Num scraped: " + str(scraped_jobs))
                    if scraped_jobs == scrapes:
                        return print("scrape finished")
        start += 10


def job_id_to_description(job_id):
    job_url = "https://www.indeed.com/viewjob?jk=" + str(job_id)
    page = requests.get(job_url)
    post_soup = BeautifulSoup(page.content, "html.parser")
    description = post_soup.find(class_="jobsearch-jobDescriptionText")
    return description.text


if __name__ == "__main__":
    main()
