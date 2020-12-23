import csv
from faker import Faker


def generate_data(records, headers):
    fake = Faker("en_US")
    with open("data.csv", "wt") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            first_name = fake.first_name()
            last_name = fake.last_name()
            writer.writerow(
                {
                    "id": i,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": fake.email(),
                    "pincode": fake.zipcode(),
                    "timestamp": fake.time(),
                }
            )


if __name__ == "__main__":
    records = 10000
    headers = ["id", "first_name", "last_name", "email", "pincode", "timestamp"]
    generate_data(records, headers)

