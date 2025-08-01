from django.db import models

class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    total_questions = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in minutes")
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )

    def __str__(self):
        return self.text


class Participant(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.mobile})"


# ✅ NEW MODEL for saving individual answers persistently
class ParticipantAnswer(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('participant', 'question')  # ensures no duplicate answers

    def __str__(self):
        return f"{self.participant} - Q: {self.question.id} => {self.selected_option}"
