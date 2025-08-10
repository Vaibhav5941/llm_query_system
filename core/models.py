from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.TextField()
    insurer = models.CharField(max_length=100, blank=True, null=True)
    uin = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Query(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.query_text[:60]

class Answer(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='answers')
    decision = models.CharField(max_length=100, blank=True, null=True)
    amount = models.CharField(max_length=100, blank=True, null=True)
    justification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to: {self.query.query_text[:40]}"

class ClauseMapping(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='clauses')
    clause_reference = models.CharField(max_length=255)
    clause_text = models.TextField()

    def __str__(self):
        return f"Clause for Answer ID {self.answer.id}"
