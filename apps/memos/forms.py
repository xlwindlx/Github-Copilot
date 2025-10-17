from django import forms
from .models import Memo


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ["title", "body", "is_public"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("제목은 비어 있을 수 없습니다.")
        if len(title) > 200:
            raise forms.ValidationError("제목은 200자 이하여야 합니다.")
        return title