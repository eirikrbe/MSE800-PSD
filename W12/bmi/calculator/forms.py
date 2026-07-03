from django import forms

class BMIForm(forms.Form):
    height = forms.FloatField(label='Height (m)', min_value=0.1, max_value=3.0)
    weight = forms.FloatField(label='Weight (kg)', min_value=0.1, max_value=600)

    def clean_height(self):
        height = self.cleaned_data['height']
        if height < 0.1 or height > 3.0:
            raise forms.ValidationError("Height must be between 0.1 and 3.0 meters.")
        return height

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight < 0.1 or weight > 600:
            raise forms.ValidationError("Weight must be between 0.1 and 600 kg.")
        return weight