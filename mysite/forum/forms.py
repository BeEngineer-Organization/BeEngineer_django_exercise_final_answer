from django import forms

from .models import Message, Tag, Comment

class TagModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class MessageForm(forms.ModelForm):
    tag = TagModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Message
        fields = [
            "content",
            "image",
        ]

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            "content",
        ]

class MessageSearchForm(forms.Form):
    keyword = forms.CharField(
        label="検索",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "メッセージで検索"}),
    )