import random

s = Storage.objects.all()[3]

for i in range(1, 11):
    Box.objects.create(name=i, storage=s, length=random.randint(2, 4), width=random.randint(2, 4),
                       height=random.randint(2, 4), price=random.randint(2000, 4000))
