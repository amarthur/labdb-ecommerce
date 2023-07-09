# Mongo DB

from djongo import models

class MongoUser(models.Model):
    _id = models.CharField(primary_key=True, max_length=100)


class MongoRating(models.Model):
    _id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(MongoUser, on_delete=models.CASCADE)
    rating = models.IntegerField()
    date = models.DateTimeField()
    comment = models.TextField()


class MongoProduct(models.Model):
    _id = models.IntegerField(primary_key=True)
    ratings = models.ArrayReferenceField(
        to=MongoRating,
        on_delete=models.CASCADE,
    )


class MongoCompany(models.Model):
    _id = models.CharField(primary_key=True, max_length=100)
    ratings = models.ArrayReferenceField(
        to=MongoRating,
        on_delete=models.CASCADE,
    )
    class Meta:
        app_label = 'app'
