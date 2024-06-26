from src.domain.repositories.client_repository_interface import ClientRepositoryInterface


class GetAllClientsNamesUseCase:
    def __init__(self, client_repository: ClientRepositoryInterface):
        self.client_repository = client_repository

    def execute(self):
        response = self.client_repository.get_all_clients()
        return [client.name for client in response]
