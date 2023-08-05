=====
Django DragonPay
=====

Django DragonPay is the wrapper for the DragonPay API that can easily be integrated with your Django application.

Quick Start
-----------

0. To install, use pip::

    pip install django_dragonpay

1. Add django_dragonpay to you INSTALLED_APPS settings like this:
    INSTALLED_APPS = [
        ...,

        'django_dragonpay',

        ...
    ]

2. Configure django_dragonpay by adding these to your settings.py::

    DRAGONPAY_TEST_MODE = False        # set to True when in test env
    DRAGONPAY_ID = "MYCOMPANY"
    DRAGONPAY_PASSWORD = "password"
    DRAGONPAY_API_KEY = "api_key"
    DRAGONPAY_ENCRYPT_PARAMS = Yes     # Enable encryption of request parameters
    DRAGONPAY_TXN_LENGTH = 20          # Length of transaction ids
    DRAGONPAY_SAVE_DATA = True         # Save transaction and payout data to database

3. If you choose to enable **DRAGONPAY_SAVE_DATA** you will need to run migrations.::

    python manage.py migrate django_dragonpay

Usage
-----
Getting Paid: SOAP (django_dragonpay.api.soap)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most methods are fairly straightforward and should be easily understood especially if you've read the DragonPay API.

To create a payment transaction and generate the transaction URl, use **get_txn_token_url**::

    from django_dragonpay.api.soap import get_txn_token_url

    def payment_creation(request):
        # do your thing here

        # params are optional
        txn_url = get_txn_token_url(
            amount, description, email, param1=param1, param2=param2)

        return redirect(txn_url)


If you only want to get the transaction token and not get the redirect url::

    from django_dragonpay.api.soap import get_txn_token

    def payment_creation(request):
        # do your thing here

        token, tnx_id = get_txn_token(amount, description, email)

        # process the tokenid here

        # then you may generate the redirect url
        txn_url = get_txn_url_from_token(tokenid)

        return redirect(txn_url)
Sending Payouts
~~~~~~~~~~~~~~~

To send a payout, use the **request_payout_ex** method::

    from django_dragonpay.api.soap import request_payout_ex

    def send_payout(request):
        # get the response and transaction id
        payout_response, txn_id = request_payout_ex(
            user_name='Juan Dela Cruz',
            amount='500.00',
            description='Take my cash',
            proc_id='BPI',
            proc_detail='4444666622',
            email='juandelacruz@gmail.com',
            mobile='09087776666'
        )

        if payout_response == '0':
            # Success
        else:
            # see constants.DRAGONPAY_PAYOUT_ERROR_CODES for the complete
            # list of ERROR_CODES for PAYOUT


When using the TEST Environment, payouts will not be completed unless you will request for DragonPay operations to update the status of the test request.

If you enable storing to database by setting **DRAGONPAY_SAVE_DATA** to **True**, everytime a successful transaction (payment, or payout), a record will be added to the database.


Logging
-------

Set the logger ``dragonpay.soap`` to **DEBUG** to see the XML response from DragonPay, and set it to **INFO** to ignore them.



DragonPay API Notes
-------------------


1. The Merchant PASSWORD or KEY is the SECRET for all Payment Switch API transactions.
2. The API KEY is used for Payouts.
