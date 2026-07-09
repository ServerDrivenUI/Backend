import logging

from faker import Faker
import faker_commerce


class StatisticService:
    def __init__(self):
        self.faker = Faker()
        self.faker.add_provider(faker_commerce.Provider)
        self.logger = logging.getLogger(__name__)
        
    async def collect(self):
        pass


statistic_service = StatisticService()
