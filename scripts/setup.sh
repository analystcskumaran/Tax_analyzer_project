#!/bin/bash
pip install -r requirements.txt
cd backend/django_app && python manage.py migrate
cd ../../models && python train_model.py