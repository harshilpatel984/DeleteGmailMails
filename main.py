from DeleteGmailMail import DeleteGmail
import json

if __name__ == '__main__':

    print("Gmail Mail Deletion")

    # Set user id and berear token
    user_id = ""
    berear_token = ""

    # Initialize Delete mail class
    mail = DeleteGmail(user_id,berear_token)

    # Print user id and berear token
    print("User Id:      {}".format(mail.getUserId()))
    print("Berear Token: {}".format(mail.getBearerToken()))

    # Get Gmail Lable List
    json_lable = mail.getGmailLable()

    # Process Gmail Lable Response
    mail.processGmailLable(json_lable)