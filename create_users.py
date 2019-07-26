import faker
import random

RECORDS = 1000000

f = faker.Faker("en_GB")

f_last  = lambda f, l: f"{f[0]}{l}{random.randint(0, 1000)}"
l_first = lambda f, l: f"{l[0]}{f}{random.randint(0, 1000)}"
first_l = lambda f, l: f"{f}{l[0]}{random.randint(0, 1000)}"
last_f  = lambda f, l: f"{l}{f[0]}{random.randint(0, 1000)}"

funcs = [f_last, l_first, first_l, last_f]
users = set()

for i in range(RECORDS):

    fn = f.first_name()
    ln = f.last_name()

    username = random.choice(funcs)(fn, ln)

    users.add(username)

with open("usernames.txt", "w") as f:
    
    f.writelines("\n".join(users))

