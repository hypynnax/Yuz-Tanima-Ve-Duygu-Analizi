from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    job = models.CharField(max_length=50)
    size = models.FloatField()
    weight = models.FloatField()
    blood_group = models.CharField(max_length=7)
    gender = models.CharField(max_length=10)

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": self.date_of_birth,
            "job": self.job,
            "size": self.size,
            "weight": self.weight,
            "blood_group": self.blood_group,
            "gender": self.gender,
        }


class UserPhoto(models.Model):
    userId = models.TextField()
    photo = models.TextField()

    def to_dict(self):
        return {
            "userId": self.userId,
            "photo": self.photo,
        }
