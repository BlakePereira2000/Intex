from django.db import models
import datetime

# Create your models here.
class Food(models.Model):
    food_name = models.CharField(max_length=200)
    sodium = models.DecimalField(max_digits=8, decimal_places=2)
    protein = models.DecimalField(max_digits=8, decimal_places=2)
    potassium = models.DecimalField(max_digits=8, decimal_places=2)
    phosphorus = models.DecimalField(max_digits=8, decimal_places=2)
    water = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) :
        return (self.food_name)

    def save(self):
        self.food_name = self.food_name.upper()
        super(Food, self).save() # Calls the "real" save() method

class Comorbidity(models.Model):
    comorbidity_name =  models.CharField(max_length=25, blank=False)
    
    def __str__(self) :
        return (self.comorbidity_name)

class User(models.Model):
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    dob = models.DateField(auto_now=True, auto_now_add=False, blank=False)
    weight = models.DecimalField(max_digits=8, decimal_places=2,blank=False)
    height = models.DecimalField(max_digits=8, decimal_places=2,blank=False)
    gender = models.CharField(max_length=1, blank=False)
    stage = models.IntegerField(default=0,blank=False)
    comorbidities = models.ManyToManyField(Comorbidity,blank=True)
    username = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=20, blank=False)

    def __str__(self) :
        return (self.first_name)

    def save(self):
        self.first_name = self.first_name.upper()
        self.last_name = self.last_name.upper()
        super(User, self).save() # Calls the "real" save() method

class Daily_Journal(models.Model):
    date = models.DateField(blank=False)
    journal_user = models.ForeignKey('User', null=False,blank=False,on_delete=models.PROTECT)
    daily_weight = models.DecimalField(max_digits=8, decimal_places=2)
    avg_blood_sugar = models.DecimalField(max_digits=8, decimal_places=2)
    lab_blood_pressure = models.DecimalField(max_digits=8, decimal_places=2)
    lab_sodium = models.DecimalField(max_digits=8, decimal_places=2)
    lab_creatinine = models.DecimalField(max_digits=8, decimal_places=2)
    lab_albumin = models.DecimalField(max_digits=8, decimal_places=2)
    lab_potassium = models.DecimalField(max_digits=8, decimal_places=2)
    lab_phosphorus = models.DecimalField(max_digits=8, decimal_places=2)
    water_intake = models.DecimalField(max_digits=8, decimal_places=2)
    daily_foods = models.ManyToManyField('Food',through='Food_in_Day')

    def __str__(self) :
        output = str(self.date)
        return (output)

class Food_in_Day(models.Model):
    journal = models.ForeignKey(Daily_Journal,on_delete=models.CASCADE)
    food = models.ForeignKey(Food,on_delete=models.CASCADE)
    grams = models.DecimalField(default=0,max_digits=8, decimal_places=2)

    def __str__(self) :
        return (str(self.journal.date) +' ' + (self.food.food_name))