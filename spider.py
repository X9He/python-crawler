from urllib.request import urlopen
from linkfinder import LinkFinder
from domain import *
from general import *


class Spider:

    # Class variables (shared among all instances) (like static variables in c++)
    project_name = ''
    base_url = ''
    domain_name = ''  # domain name of the site you're crawling on, there are python tools to help
    queue_file = ''  # text file on hard drive
    crawled_file = ''  # text file on hard drive
    queue = set()  # all the pages in queue
    crawled = set()  # all the pages crawled
    # no need to set value yet because declaring, any spider can set the value of these

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        # the above won't change for any spider
        self.boot()
        self.crawl_page('First spider', Spider.base_url)
        # the first base url crawl does not need multiple spiders

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' is crawling on ' + page_url + '\n')
            print('Queue ' + str(len(Spider.queue)) + " | Crawled: " + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            # print(response.getheader('Content-Type'))
            # print(type(response.getheader('Content-Type')))
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            # print('this is never executed \n' + url)
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
