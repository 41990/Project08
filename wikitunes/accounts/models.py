from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
import os
from datetime import datetime



class AccountUser(models.Model):
    bio

