from dotenv import load_dotenv
from github import Auth, Github
from os import getenv
import networkx


class Github_API:

    def __init__(self, token, user, repo) -> None:
        self.auth= Auth.Token(token)
        self.user = user
        self.repo = repo

    def start(self) -> None:
        self.session = Github(auth=self.auth, per_page=100)
        self.get_stargazers()

    def stop(self) -> None:
        self.session.close()

    def get_stargazers(self):
        stargazers = [stargazer for stargazer in self.session.get_user(self.user).get_repo(self.repo).get_stargazers()]


if "__main__" == __name__:
    load_dotenv()
    token = getenv("token")
    user = "ptwobrussell"
    repo = "Mining-the-Social-Web"
    CRAWL_DA_SOCIAL_WEB = Github_API(token, user, repo)
    CRAWL_DA_SOCIAL_WEB.start()
    CRAWL_DA_SOCIAL_WEB.stop()

