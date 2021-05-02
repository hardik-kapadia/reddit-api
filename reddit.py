from re import S
import praw
from praw.reddit import Submission, Subreddit, Redditor

from pathvalidate import sanitize_filepath

from tqdm import tqdm
import requests

from gfycat.client import GfycatClient
from gfycat.error import GfycatClientError

# Store your API keys in a config.py module and use the module to access them (for security)
# Comment out the next line if you don't want to
# import config as conf

import os


class reddit_api:

    __reddit = None
    __gfycat = None

    def __init__(self, reddit, gfy):
        self.__reddit = reddit
        self.__gfycat = gfy

    @classmethod
    def get_instance(cls, client_id, client_secret, user_agent, username, password):
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent,
                             username=username,
                             password=password)
        return cls(reddit, None)

    @classmethod
    def get_instance_with_gfy(cls, client_id, client_secret, user_agent, username, password, gfy_id, gfy_secret):
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent,
                             username=username,
                             password=password)

        client = GfycatClient(gfy_id, gfy_secret)

        return cls(reddit, client)

    def get_posts(self, subreddit, words, limit):

        fsubr = self.__reddit.subreddit(subreddit)

        if not os.path.exists(subreddit):
            os.makedirs(subreddit)

        t_count = 0
        c_count = 0

        submissions = []

        for submission in fsubr.hot(limit=limit):

            title = submission.title
            # print("Title:", title)

            if self.__contains_keys(words, title):

                if(submission.is_self):
                    reddit_api.createText(submission, subreddit)
                    submissions.append(submission)
                else:
                    if(self.__is_img(submission.url)):

                        reddit_api.__download_img(
                            submission.url, title, subreddit)
                        t_count += 1
                        submissions.append(submission)

            else:

                submission.comments.replace_more(limit=0)
                for comment in submission.comments:

                    if reddit_api.__contains_keys(words, comment.body):

                        c_count += 1

                        if(submission.is_self):
                            reddit_api.createText(submission, subreddit)
                            submissions.append(submission)
                        else:

                            if(self.__is_img(submission.url)):

                                reddit_api.__download_img(
                                    submission.url, title, subreddit)
                                submissions.append(submission)

                                break

        return submissions, t_count, c_count

    def __is_img(self, url):

        supported_formats = ['png', 'gif', 'gifv', 'jpg', 'jpeg']
        for supported_format in supported_formats:
            if url.endswith('.'+supported_format):

                # print(url, 'ends with', supported_format)
                return True
        if not self.__gfycat:
            return False
        else:
            return 'gfycat.com' in url

    @staticmethod
    def createText(submission, subreddit):
        title = submission.title
        filename = subreddit+"/"+title+".txt"
        filename = sanitize_filepath(filename)
        f = open(filename, "w")
        text = submission.selftext
        f.write(text)
        f.close()

    @staticmethod
    def __download_img(url, title, folder):
        
        buffer_size = 1024

        if('gfycat.com' in url):
            url = reddit_api.__get_download_gfy(url)

        response = requests.get(url, stream=True)

        file_size = int(response.headers.get("Content-Length", 0))
        filename = url.split("/")[-1]
        filename = folder+'/'+title+'.'+(url.split('.')[-1])
        filename = sanitize_filepath(filename)

        progress = tqdm(response.iter_content(buffer_size),
                        f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)

        with open(filename, "wb") as f:
            for data in progress:
                f.write(data)
                progress.update(len(data))

    def __get_download_gfy(self, url):

        url = url.split('/')[-1]

        gif = self.__gfycat.query_gfy(url)

        return gif['gfyItem']['gifUrl']

    @staticmethod
    def __contains_keys(words, str):

        for word in words:
            word_c = len(word.split(' '))

            if(len(str.split(' ')) <= word_c):
                if str.lower() == word.lower():
                    return True
                else:
                    continue
            split_ = str.split(' ')
            for i in range(len(split_) - word_c + 1):
                stemp = ''

                for j in range(word_c):
                    stemp += split_[i+j]+' '

                stemp = stemp[0:-1]

                if stemp.lower().strip() == word.lower().strip():
                    return True
        return False
