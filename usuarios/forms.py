#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',}) )