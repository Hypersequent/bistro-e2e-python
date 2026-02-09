from faker import Faker

fake = Faker()


class UserData:
    def get_name(self) -> str:
        return fake.name()

    def get_address(self) -> str:
        return fake.street_address()
