from django.db import models


class Subsystem(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    def dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }


class Folder(models.Model):
    subsystem = models.ForeignKey(to='Subsystem', on_delete=models.PROTECT, db_index=True)
    name = models.CharField(max_length=250, db_index=True)

    def dict(self, subsystem_in: bool = False) -> dict:
        return {
            'id': self.id,
            'subsystem_id': self.subsystem_id,
            'subsystem': self.subsystem.dict() if subsystem_in else None,
            'name': self.name
        }


class Task(models.Model):
    folder = models.ForeignKey(to='Folder', on_delete=models.PROTECT, db_index=True)
    roles = models.ManyToManyField(to='Role', db_index=True, blank=True)
    name = models.CharField(max_length=250, db_index=True)

    def dict(self, folder_in: bool = False) -> dict:
        return {
            'id': self.id,
            'folder_id': self.folder_id,
            'folder': self.folder.dict(folder_in) if folder_in else None,
            'name': self.name,
        }


class Segment(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    def dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }


class Attachment(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    segment = models.ForeignKey(to='Segment', on_delete=models.PROTECT, db_index=True)

    def dict(self, segment_in: bool = False) -> dict:
        return {
            'id': self.id,
            'segment_id': self.segment_id,
            'attachment': self.segment.dict() if segment_in else None,
            'name': self.name
        }


class Role(models.Model):
    attachment = models.ForeignKey(to='Attachment', on_delete=models.PROTECT, db_index=True)
    templates = models.ManyToManyField(to='Template', db_index=True, blank=True)
    name = models.CharField(max_length=250, db_index=True)

    def dict(self, attachment_in: bool = False) -> dict:
        return {
            'id': self.id,
            'attachment_id': self.attachment_id,
            'attachment': self.attachment.dict(attachment_in) if attachment_in else None,
            'name': self.name
        }


class Template(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    def dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
