from django import forms
from django.contrib import admin
from django.shortcuts import redirect, get_object_or_404
from .models import ChatSupport
from chats.models import Chat

class ChatReplyForm(forms.Form):
    new_message = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "cols": 80}), required=False)

class ChatSupportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'last_message', 'is_open', 'created_date')
    readonly_fields = ('employee', 'last_message', 'is_open', 'created_date')
    change_form_template = "admin/support/chat_support/change_form.html"  # Custom template

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = get_object_or_404(ChatSupport, pk=object_id)
        extra_context = extra_context or {}

        # Get related chat messages
        related_chats = Chat.objects.filter(employee=obj.employee)
        extra_context['related_chats'] = related_chats

        # Handle form submissions
        if request.method == "POST":
            if 'send_reply' in request.POST:
                form = ChatReplyForm(request.POST)
                if form.is_valid():
                    new_message = form.cleaned_data['new_message']
                    if new_message:
                        Chat.objects.create(
                            employee=obj.employee,
                            agency=obj.employee.agency,
                            message=new_message,
                            sender='AI',
                            is_support=True
                        )
                    return redirect(request.path)

            elif 'close_ticket' in request.POST:
                # Handle closing the ticket
                obj.is_open = False
                obj.save()
                Chat.objects.create(
                    employee=obj.employee,
                    agency=obj.employee.agency,
                    message="systeminfo$:$chat$:$Salamat, Mag sabi ka lang ulit kung magkaron ka ng problema.",
                    sender='AI',
                    is_support=True
                )
                return redirect(request.path)

        else:
            form = ChatReplyForm()

        extra_context['form'] = form

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

admin.site.register(ChatSupport, ChatSupportAdmin)
