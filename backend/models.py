from django.db import models


class Subsystem(models.Model):
    name = models.CharField(max_length=250, db_index=True)


class Folder(models.Model):
    subsystem = models.ForeignKey(to='Subsystem', on_delete=models.PROTECT, db_index=True)
    name = models.CharField(max_length=250, db_index=True)


class Task(models.Model):
    folder = models.ForeignKey(to='Folder', on_delete=models.PROTECT, db_index=True)
    roles = models.ManyToManyField(to='Role', db_index=True, blank=True)
    name = models.CharField(max_length=250, db_index=True)


class Segment(models.Model):
    name = models.CharField(max_length=250, db_index=True)


class Attachment(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    segment = models.ForeignKey(to='Segment', on_delete=models.PROTECT, db_index=True)


class Role(models.Model):
    attachment = models.ForeignKey(to='Attachment', on_delete=models.PROTECT, db_index=True)
    templates = models.ManyToManyField(to='Template', db_index=True, blank=True)
    name = models.CharField(max_length=250, db_index=True)


class Template(models.Model):
    name = models.CharField(max_length=250, db_index=True)
