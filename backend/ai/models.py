from django.db import models
import uuid


class AIChatLog(models.Model):
    """Log all AI chat interactions."""
    session_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    user_message = models.TextField()
    ai_response = models.TextField()
    language = models.CharField(max_length=10, default='en')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "AI Chat Log"
        verbose_name_plural = "AI Chat Logs"
    
    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.user_message[:50]}"
