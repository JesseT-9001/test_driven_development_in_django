"""
This modules handles all the forms for the hashing web-app.
"""

from django import forms


class HashForm(forms.Form):
    """
    Creates textbox to accept user input.

    :var form text: hold form text area.
    """
    text = forms.CharField(label='Enter hash here:', widget=forms.Textarea)