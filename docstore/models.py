import uuid

from django.db import models

# Create your models here.

"""
Note - To simplify the model design, these models use UUIDs as their IDs, and as
their primary keys. UUIDs as primary keys may lead to poor performance on
associated foreign key lookups in Postgres. In addition, it affects data
locality on disk for neighboring records. This is probably not an issue for a
rapid prototype, but if this is going to be used at
scale, making the UUID its own property with a secondary index on it that is used
solely for external identifiers and keeping the record ID (and PK) as type
serial should be looked into.
"""

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    short_desc = models.CharField(max_length=255)
    full_desc = models.TextField()

    def __str__(self):
        return self.short_desc


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    topics = models.ManyToManyField(Topic)

    def __str__(self):
        return self.name

    def absolute_path(self) -> str:
        path = '/' + self.name
        if self.parent is not None:
            path = self.parent.absolute_path() + path
        return path


class Document(models.Model):
    """
    Document looks very similar to Folder except that field 'parent' is replaced
    with field 'folder'. It is possible the two could be combined, but this
    could lead to worse readability at the cost of only marginal performance
    gain, if any.

    THE 'contents' FIELD:
    ---------------------
    This model implies storeing document contents directly in the database. This
    is an extremely poor design in almost all cases, but as this is merely a
    prototype, it will be allowed for this case. It will lead to abyssmal
    database performance. For actual implementation, consider replacing this
    field with perhaps a "filename_on_disk" field which would refer to where the
    file is on disk. If further extensibility is needed, consider replacing
    direct filesystem lookup with a file-retrieval service.

    Alternatively, if the requirement that an RDBMS be used is flexible, it's
    possible that a document-oriented NoSQL DB such as MongoDB may be better for
    this system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    topics = models.ManyToManyField(Topic)
    
    # See class comment for justification on use of BinaryField
    contents = models.BinaryField(editable=False)

    def __str__(self):
        return self.name

    