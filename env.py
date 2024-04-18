from dotenv import dotenv_values

mysqlhost = dotenv_values(".env")["MYSQL_HOST"]
mysqluser = dotenv_values(".env")["MYSQL_USER"]
mysqlpass = dotenv_values(".env")["MYSQL_PASSWORD"]
mysqltablename = dotenv_values(".env")["MYSQL_TABLE_NAME"]
mysqldb = dotenv_values(".env")["MYSQL_DATABASE"]

account_sid = dotenv_values(".env")["twilio_account_sid"]
auth_token = dotenv_values(".env")["twilio_auth_token"]
twilio_phone_number = dotenv_values(".env")["twilio_phone_number"]
to_phone_number = dotenv_values(".env")["twilio_to_phone_number"]