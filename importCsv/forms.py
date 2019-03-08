from django import forms

class uploadForm(forms.Form):
    title = forms.CharField(max_length=50)
    csv_file = forms.FileField(required=True, label='upload csv file')

class upload_url(forms.Form):
    title = forms.CharField(max_length=50)
    url = forms.CharField(max_length=1000)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
    save = forms.BooleanField(required=False)


class searchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cities = kwargs.pop('cities', None)
        super().__init__(*args, **kwargs)
        for i, city in enumerate(cities):
            self.fields['%s' % city.abbrev] = forms.CharField(label=city,required=False)