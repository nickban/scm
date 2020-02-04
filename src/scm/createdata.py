import copy
from models import Sample
from django.contrib.auth import settings


def copysample():
    sample = Sample.objects.get(pk=14)
    for i in range(1, 100):
        copy.copy(sample)


if __name__ == '__main__':
    copysample()
