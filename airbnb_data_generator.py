import json
import boto3
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
fake = Faker()

#defining the sqs client
sqs_client = boto3.client('sqs')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/339712975909/gds-ade-airbnb-booking-queue'  # replace with your SQS Queue URL


# main handler funtion
def lambda_handler(event, context):
    i=0
    while(i<5):
        booking = generate_bookings()
        print(booking)
        sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(booking)
        )
        i += 1
    
    return {
        'statusCode': 200,
        'body': json.dumps('Booking order published to SQS!')
    }


def generate_bookings():
    start_end_date = generate_dates()
    return {
        "booking_id": generate_booking_id(),
        "user_id": generate_user_id(),
        "property_id": generate_property_id(),
        "location": generate_location(),
        "start_date": start_end_date[0],
        "end_date": start_end_date[1],
        "price": generate_price()
    }


def generate_booking_id():                  #generates random booking id
    return f"B_{uuid.uuid4().fields[-1]//100000}"

def generate_user_id():                     #generates random user id
    return f"U_{uuid.uuid4().fields[-1]//100000}"

def generate_property_id():                 #generates random property id
    return f"P_{uuid.uuid4().fields[-1]//100000}"

def generate_location():                    #generates random city, country
    return fake.city() + ", " + fake.country()

def generate_dates():                       #generates random start and end date as tuple
    start_date = fake.date_between(start_date='-30d', end_date='today')
    end_date = start_date + timedelta(days=random.randint(1, 14))
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

def generate_price():                       #generates random booking price
    return round(random.uniform(10, 100), 2)