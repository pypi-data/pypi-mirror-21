import os

import github
import github.GithubObject
import json
import yaz

from .version import __version__
from .spreadsheet import VersionMatrixSheet
from .github import Github
from .log import set_verbose

__all__ = ["DependencyMatrix"]


class DependencyMatrix(yaz.BasePlugin):
    json_key_file = None
    sheet_key = None

    def __init__(self):
        if not (self.json_key_file and self.sheet_key):
            raise RuntimeError("The json_key_file and sheet_key must be specified, please add a DependencyMatrix plugin override in your user directory")

    @yaz.dependency
    def set_github(self, github: Github):
        self.github = github.get_service()

    @yaz.task
    def version(self, verbose: bool = False):
        set_verbose(verbose)
        return __version__

    @yaz.task
    def update_spreadsheet(self, limit: int = 666, verbose: bool = False):
        set_verbose(verbose)

        sheet = VersionMatrixSheet(os.path.expanduser(self.json_key_file), self.sheet_key)
        sheet.set_updating()
        try:
            for repo in self.get_repos()[:limit]:
                dependencies = self.get_dependencies(repo)
                if dependencies:
                    sheet.set_dependencies(repo, dependencies)
        finally:
            sheet.unset_updating()

    def get_repos(self):
        return self.github.get_user().get_repos()

    def get_dependencies(self, repo, ref=github.GithubObject.NotSet):
        try:
            file = repo.get_file_contents('/composer.lock', ref)
        except github.GithubException:
            return {}
        data = json.loads(file.decoded_content.decode())

        return {package['name']: package['version'].strip() for package in data['packages']}
