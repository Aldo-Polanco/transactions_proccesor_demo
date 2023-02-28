==============
# Transaction Account Manager Demo
==============

This app let you upload your transaction files to the app to be proccesed and send you a resume to your email.

==============
## CSV example format
==============

The csv file should have the following schema

Id,Date,Transaction\
0,7/15,+672.25\
1,7/28,-102.73\
2,8/2,-450.8\
3,8/8,+9804.55\

==============
## Setup
==============

Before anything make sure that you have already set this env variables before runing the docker-compose command, by example:

    $ export DB_USERNAME="postgres" \
    $ export DB_PASSWORD="123456" \
    $ export DB_NAME="demo" \
    $ export APP_SECRET="miaw" \
    $ export SENDER_EMAIL="aldo.polanco@zohomail.com" \
    $ export SENDER_EMAIL_PASS="your_password" \
    $ export SMTP_SERVER="smtp.zoho.com" \

==============
## How to Run
==============

then you can just run like this

    $ docker-compose up

After this you can acces at your browser at 0.0.0.0:5000

You can make an account and then you can upload your csv to be proccesed.
