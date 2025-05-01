from dotenv import load_dotenv
from github import Auth, Github
from os import getenv
import networkx


class Github_API:

    def __init__(self, token, users, repos) -> None:
        self.auth= Auth.Token(token)
        self.usernames = users
        self.repositories = repos

    def start(self) -> None:
        combination = list()
        combo_g = networkx.DiGraph()
        combo_stargazers = list()
        self.session = Github(auth=self.auth, per_page=100)
        for self.username, self.repository in zip(self.usernames, self.repositories):
            user, repo, stargazers = self.get_stargazers()
            combination.append(self.build_graph(user, repo, stargazers))
        for graph, gazers in combination:
            combo_g = networkx.compose(combo_g, graph)
            combo_stargazers.extend(gazers)
        self.get_relations(combo_g, combo_stargazers)
        networkx.write_graphml(combo_g, f"github.graphml")

    def stop(self) -> None:
        self.session.close()

    def get_stargazers(self) -> tuple:
        user = self.session.get_user(self.username)
        repo = user.get_repo(self.repository)
        stargazers = [stargazer for stargazer in repo.get_stargazers()]
        return user, repo, stargazers

    def build_graph(self, user, repo, stargazers) -> tuple:
        g = networkx.DiGraph()
        g.add_node(repo.name + "(repo)", type="repo", lang=repo.language, owner=user.login)
        for gazer in stargazers:
            g.add_node(gazer.login + "(user)", type="user")
            g.add_edge(gazer.login + "(user)", repo.name + "(repo)", type="gazes")
        return g, stargazers

    def get_relations(self, g, stargazers) -> None:
        for gazer in stargazers:
            try:
                for follower in gazer.get_followers():
                    if follower.login + "(user)" in g:
                        g.add(follower.login + "(user)", gazer.login + "(user)", type="follows")
            except Exception:
                print(Exception)
        return g


if "__main__" == __name__:
    load_dotenv()
    token = getenv("token")
    users = ["mikhailklassen", "ptwobrussell"]
    repos = ["Mining-the-Social-Web-3rd-Edition", "Mining-the-Social-Web-2nd-Edition"]
    CRAWL_DA_SOCIAL_WEB = Github_API(token, users, repos)
    CRAWL_DA_SOCIAL_WEB.start()
    CRAWL_DA_SOCIAL_WEB.stop()

