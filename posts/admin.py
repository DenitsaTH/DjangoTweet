from django.contrib import admin

from posts.models import Post


class CustomPostsAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'created_at',
                    'is_deleted', 'deleted_at', 'author']
    list_filter = ['is_deleted']
    search_fields = ['id', 'author', 'content']
    actions = ['restore_posts']

    @admin.action(description='Restore deleted posts')
    def restore_posts(self, request, queryset):
        posts_restored = queryset.update(is_deleted=False)
        self.message_user(request, f"{posts_restored} posts restored.")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=True)


admin.site.register(Post, CustomPostsAdmin)
