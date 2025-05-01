from dotenv import load_dotenv
from github import Auth, Github
from os import getenv


class Github_API:

    def __init__(self, token, user, repo) -> None:
        self.auth = Auth.Token(token)
        self.user = user
        self.repo = repo

    def authorize(self) -> None:
        g = Github(auth=self.auth)
        print(g.get_user(self.user).get_repo(self.repo))
        g.close()


if "__main__" == __name__:
    load_dotenv()
    token = getenv("token")
    user = "ptwobrussell"
    repo = "Mining-the-Social-Web"
    CRAWL_DA_WEB = Github_API(token, user, repo)
    CRAWL_DA_WEB.authorize()

