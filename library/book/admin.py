from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'count',
        'get_authors'
    )

    search_fields = (
        'id',
        'name',
        'authors__name',
        'authors__surname'
    )

    list_filter = (
        'authors',
    )

    fieldsets = (
        ('Static information', {
            'fields': (
                'name',
                'description',
                'authors'
            )
        }),

        ('Changeable information', {
            'fields': (
                'count',
            )
        }),
    )

    def get_authors(self, obj):
        return ", ".join(
            [f"{author.name} {author.surname}"
             for author in obj.authors.all()]
        )

    get_authors.short_description = 'Authors'