from django.contrib import admin
from .models import Players, Comment

# Register your models here.
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('name', 'back_number')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('players', 'user', 'content', 'created_at')

admin.site.register(Players, PlayersAdmin)
admin.site.register(Comment, CommentAdmin)