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
        print(self.session.rate_limiting)
        print(self.session.rate_limiting_resettime)
        # user, repo, stargazers = self.get_stargazers()
        # self.build_graph(user, repo, stargazers)

    def stop(self) -> None:
        self.session.close()

    def get_stargazers(self) -> tuple:
        user = self.session.get_user(self.user)
        repo = user.get_repo(self.repo)
        stargazers = [stargazer for stargazer in repo.get_stargazers()]
        return user, repo, stargazers

    def build_graph(self, user, repo, stargazers) -> None:
        g = networkx.DiGraph()
        g.add_node(repo.name + "(repo)", type="repo", lang=repo.language, owner=user.login)
        for gazer in stargazers:
            g.add_node(gazer.login + "(user)", type="user")
            g.add_edge(gazer.login + "(user)", repo.name + "(repo)", type="gazes")
        g = self.get_relations(g, stargazers)
        networkx.write_graphml(g, "github.graphml")

    def get_relations(self, g, stargazers) -> None:
        for gazer in stargazers:
            for follower in gazer.get_followers():
                if follower.login + "(user)" in g:
                    g.add(follower.login + "(user)", gazer.login + "(user)", type="follows")
        return g


if "__main__" == __name__:
    load_dotenv()
    token = getenv("token")
    user = "mikhailklassen"
    repo = "Mining-the-Social-Web-3rd-Edition"
    CRAWL_DA_SOCIAL_WEB = Github_API(token, user, repo)
    CRAWL_DA_SOCIAL_WEB.start()
    CRAWL_DA_SOCIAL_WEB.stop()

