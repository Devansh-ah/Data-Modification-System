from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.


class Aadhar(models.Model):
    Aadhar_Number = models.BigIntegerField(
        validators=[MaxValueValidator(999999999999)], primary_key=True)
    Image = models.ImageField(upload_to='dms/images', default='')
    fName = models.CharField(max_length=50, default='abcd')
    mName = models.CharField(max_length=50, default='xyz')
    lName = models.CharField(max_length=50, default='pqrs')
    Age = models.IntegerField()
    Sex = models.CharField(max_length=6)
    DOB = models.DateField()
    Mobile_NUmber = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999)])
    Enrollment_Number = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999)])
    QR_code = models.ImageField(upload_to='dms/images', default='')
    Bar_Code = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    fp_Actualdata = models.ImageField(upload_to='dms/images', default='')


class DrivingLicence(models.Model):
    LicenceNo = models.CharField(max_length=15)
    AadharNo = models.ForeignKey(Aadhar, on_delete=models.CASCADE, validators=[
                                 MaxValueValidator(999999999999)])
    Pic = models.ImageField(upload_to='dms/images', default='')
    DateOfFirstIssue = models.DateField()
    DOB = models.DateField()
    contactInfo = models.BigIntegerField(
        validators=[MaxValueValidator(99999999999)])
    validity = models.IntegerField()
    fName = models.CharField(max_length=50, default='abcd')
    mName = models.CharField(max_length=50, default='xyz')
    lName = models.CharField(max_length=50, default='pqrs')
    Personal = models.BooleanField(default=True)
    Commercial = models.BooleanField(default=False)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pinCode = models.IntegerField()


class VoterId(models.Model):
    Bar_Code = models.CharField(max_length=13)
    AadharNo = models.ForeignKey(Aadhar, on_delete=models.CASCADE, validators=[
                                 MaxValueValidator(999999999999)])
    Pic = models.ImageField(upload_to='dms/images', default='')
    fName = models.CharField(max_length=50, default='abcd')
    mName = models.CharField(max_length=50, default='xyz')
    lName = models.CharField(max_length=50, default='pqrs')
    FathersName = models.CharField(max_length=100)
    DOB = models.DateField()
    Sex = models.CharField(max_length=6)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pinCode = models.IntegerField()


class Ration(models.Model):
    QR_code = models.ImageField(upload_to='dms/images', default='')
    AadharNo = models.ForeignKey(Aadhar, on_delete=models.CASCADE, validators=[
                                 MaxValueValidator(999999999999)])
    fName = models.CharField(max_length=50, default='abcd')
    mName = models.CharField(max_length=50, default='xyz')
    lName = models.CharField(max_length=50, default='pqrs')
    HOF_name = models.CharField(max_length=100)
    HOF_relation = models.CharField(max_length=50)
    Father_or_Husband = models.BooleanField(default=False)
    name_F_or_H = models.CharField(max_length=100)
    dealersName = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pinCode = models.IntegerField()


class PanCard(models.Model):
    QR_code = models.ImageField(upload_to='dms/images', default='')
    AadharNo = models.ForeignKey(Aadhar, on_delete=models.CASCADE, validators=[
                                 MaxValueValidator(999999999999)])
    fName = models.CharField(max_length=50, default='abcd')
    mName = models.CharField(max_length=50, default='xyz')
    lName = models.CharField(max_length=50, default='pqrs')
    PRNnumber = models.CharField(max_length=15)
    DOB = models.DateField()
    signature = models.ImageField(upload_to='dms/images', default='')
    pic = models.ImageField(upload_to='dms/images', default='')


class Admin(models.Model):
    eid = models.IntegerField()
    ename = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class user(models.Model):
    Aadhar_Number = models.ForeignKey(Aadhar, on_delete=models.CASCADE, validators=[
                                      MaxValueValidator(999999999999)])
    AppId = models.IntegerField()
    message_senders_id = models.IntegerField()
    message_senders_name = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    System_message = models.CharField(max_length=200)


class signup(models.Model):
    Aadhar_Number = models.BigIntegerField(
        validators=[MaxValueValidator(999999999999)])
    fp_User = models.ImageField(upload_to='dms/images', default='')


class ImageModel(models.Model):
    image = models.ImageField(upload_to='dms/temp', null=False, blank=True)
    AadharNo = models.BigIntegerField(
        validators=[MaxValueValidator(999999999999)])


class aadharQ(models.Model):
    AadharNo = models.BigIntegerField(
        validators=[MaxValueValidator(999999999999)], default=123)
    FirstName = models.CharField(max_length=100)
    MidName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    address_proof = models.ImageField(upload_to='dms/images', default='')
    Sex = models.CharField(max_length=6, default='male')
    Mobile_Number = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999)], default=9796959493)
    DOB = models.DateField(default='2000-01-01')
    birth_proof = models.ImageField(upload_to='dms/images', default='')


class voteridQ(models.Model):
    FirstName = models.CharField(max_length=100)
    MidName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    Sex = models.CharField(max_length=6, default='male')
    FathersName = models.CharField(max_length=100, default='')
    DOB = models.DateField(default='2000-01-01')


class licenceQ(models.Model):
    FirstName = models.CharField(max_length=100)
    MidName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    Mobile_NUmber = models.BigIntegerField(
        validators=[MaxValueValidator(9999999999)], default=9796959493)
    DOB = models.DateField(default='2000-01-01')


class pancardQ(models.Model):
    FirstName = models.CharField(max_length=100)
    MidName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    DOB = models.DateField(default='2000-01-01')


class RationQ(models.Model):
    FirstName = models.CharField(max_length=100)
    MidName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pincode = models.IntegerField()
    HOF_name = models.CharField(max_length=100)
    HOF_relation = models.CharField(max_length=50)
    Father_or_Husband = models.BooleanField(default=False)
    name_F_or_H = models.CharField(max_length=100)
    DOB = models.DateField(default='2000-01-01')


class userlogin(models.Model):
    AadharNo = models.BigIntegerField(
        validators=[MaxValueValidator(999999999999)])
    password = models.CharField(max_length=100)


class AdminInfo(models.Model):
    EmpId = models.CharField(max_length=100)
    fName = models.CharField(max_length=50, default='abcd')
    mName = models.CharField(max_length=50, default='xyz')
    lName = models.CharField(max_length=50, default='pqrs')
    DocName = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='dms/images', default='')


class signup1(models.Model):
    EmpId = models.CharField(max_length=100)
    fp_User = models.ImageField(upload_to='dms/images', default='')


class aadhar_status(models.Model):
    Actual_AadharNo = models.BigIntegerField(
        validators=[MaxValueValidator(999999999999)])
    AadharNo = models.CharField(max_length=10)
    FirstName = models.CharField(max_length=10)
    MidName = models.CharField(max_length=10)
    LastName = models.CharField(max_length=10)
    Street = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    address_proof = models.CharField(max_length=10)
    Sex = models.CharField(max_length=10)
    Mobile_Number = models.CharField(max_length=10)
    DOB = models.CharField(max_length=10)
    birth_proof = models.CharField(max_length=10)
