from django.contrib import admin
from django.contrib.auth.models import User 
from .models import Case, CaseComment

class CaseCommentInline(admin.TabularInline):
    model = CaseComment
    extra = 1  # Display an empty form to add one more comment
    readonly_fields = ('created_date',)

    # Override the formfield to automatically set the author to the logged-in user
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["initial"] = request.user.id
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # Automatically set the author to the logged-in user when saving a comment
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

class CaseAdmin(admin.ModelAdmin):
    list_display = ('category', 'employee', 'updated_date', 'date_reported', 'report_status', 'agency', 'last_comment')
    search_fields = ('category', 'employee__first_name', 'employee__last_name', 'report_status', 'agency__username')
    list_filter = ('report_status', 'updated_date', 'date_reported', 'agency')
    exclude = ('author',)
    readonly_fields = ('updated_date', 'date_reported')
    
    inlines = [CaseCommentInline]  # Add the CaseCommentInline to CaseAdmin

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Agency').exists():
            return qs.filter(agency=request.user)
        return qs

    def save_model(self, request, obj, form, change):
        if not change or not obj.agency:
            obj.agency = request.user
            obj.author = request.user
        super().save_model(request, obj, form, change)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'agency' in form.base_fields:
            del form.base_fields['agency']
        return form
    

    def last_comment(self, obj):
        last_comment = obj.comments.order_by('-created_date').first()  # Get the most recent comment
        return last_comment.text if last_comment else "No comments yet"

    last_comment.short_description = "Last Comment"

admin.site.register(Case, CaseAdmin)
