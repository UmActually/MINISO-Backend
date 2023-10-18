from faker import Faker

fake = Faker(locale="es_MX")

for _ in range(4):
    print(fake.date_time_this_month())
