from django.db import models

# Create your models here.

class Acquisitiontime(models.Model):
    timeid = models.CharField(primary_key=True, max_length=25)
    starttime = models.CharField(max_length=25, blank=True, null=True)
    endtime = models.CharField(max_length=25, blank=True, null=True)
    date = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acquisitiontime'

class Bandwidth(models.Model):
    channelid = models.CharField(primary_key=True, max_length=15)
    wavelength1 = models.FloatField(blank=True, null=True)
    wavelength2 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bandwidth'


class Endpoint(models.Model):
    endpointid = models.AutoField(primary_key=True)
    channelid = models.ForeignKey(Bandwidth, models.DO_NOTHING, db_column='channelid', blank=True, null=True)
    pexid = models.ForeignKey('Patienttreatment', models.DO_NOTHING, db_column='pexid', blank=True, null=True)
    oxyvalue = models.FloatField(blank=True, null=True)
    deoxyvalue = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'endpoint'


class Patient(models.Model):
    patientid = models.CharField(primary_key=True, max_length=10)
    patientname = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'patient'


class Patienttreatment(models.Model):
    pexid = models.CharField(primary_key=True, max_length=15)
    patientid = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patientid', blank=True, null=True)
    exerciseid = models.ForeignKey('Treatment', models.DO_NOTHING, db_column='exerciseid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patienttreatment'


class Session(models.Model):
    sessionid = models.CharField(primary_key=True, max_length=15)
    timeid = models.ForeignKey(Acquisitiontime, models.DO_NOTHING, db_column='timeid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'session'


class Treatment(models.Model):
    exerciseid = models.CharField(primary_key=True, max_length=10)
    exercisetype = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'treatment'


class Treatmentbandwidth(models.Model):
    exerciseid = models.OneToOneField(Treatment, models.DO_NOTHING, db_column='exerciseid', primary_key=True)
    channelid = models.ForeignKey(Bandwidth, models.DO_NOTHING, db_column='channelid')

    class Meta:
        managed = False
        db_table = 'treatmentbandwidth'
        unique_together = (('exerciseid', 'channelid'),)        

       