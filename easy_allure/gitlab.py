import os
import re
from abc import ABC, abstractmethod
from http import HTTPStatus

import requests

from .logger import get_logger

LOGGER = get_logger()


class GitlabException(Exception):
    pass


class BaseCIIntegration(ABC):
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url

    @abstractmethod
    def add_link_to_description(self) -> None:
        pass


class Gitlab(BaseCIIntegration):
    def __init__(self, api_url: str, token: str) -> None:
        super().__init__(api_url)
        self.token = token

    def get_description(self, ci_project_id: str, mr_iid: str) -> str:
        url = f'{self.api_url}/projects/{ci_project_id}/merge_requests/{mr_iid}'
        response = requests.get(url, headers={'PRIVATE-TOKEN': self.token})
        if response.status_code != HTTPStatus.OK:
            raise GitlabException(f'Failed to get MR description: {response.data}')
        return response.json()['description']

    def update_description(self, ci_project_id: str, mr_iid: str, description: str) -> None:
        url = f'{self.api_url}/projects/{ci_project_id}/merge_requests/{mr_iid}'
        response = requests.put(url, headers={'PRIVATE-TOKEN': self.token},
                                json={'description': description})
        if response.status_code != HTTPStatus.OK:
            raise GitlabException(f'Failed to update MR description: {response.data}')

    def add_link_to_description(self, ci_project_id: str, mr_iid: str, link: str) -> None:
        current_description = self.get_description(ci_project_id, mr_iid)

        allure_endpoint = os.environ.get('ALLURE_ENDPOINT')
        if allure_endpoint in current_description:
            new_description = re.sub(r'{0}/launch/\d+'.format(allure_endpoint), link, current_description)
        else:
            new_description = current_description + f'\n\nLast Testops launch - {link}'
        self.update_description(ci_project_id, mr_iid, new_description)
