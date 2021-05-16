import requests
import json

class DeleteGmail:

    def __init__(self,user_id,bearer_token):
        self.user_id = user_id
        self.bearer_token = bearer_token

    def getUserId(self):
        return self.user_id

    def getBearerToken(self):
        return self.bearer_token

    def getGmailLable(self):
        url = "https://gmail.googleapis.com/gmail/v1/users/{}/labels".format(self.user_id)

        payload = {}
        headers = {'Authorization': 'Bearer {}'.format(self.bearer_token)}

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    def getGmailwithLableFilter(self,lable_id):
        url = "https://gmail.googleapis.com/gmail/v1/users/{}/messages?labelIds={}".format(self.user_id,lable_id)

        payload = {}
        headers = {'Authorization': 'Bearer {}'.format(self.bearer_token)}

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    def getNextPageGmailMails(self,next_page_token):
        url = "https://gmail.googleapis.com/gmail/v1/users/{}/messages?pageToken={}".format(self.user_id,next_page_token)

        payload = {}
        headers = {'Authorization': 'Bearer {}'.format(self.bearer_token)}

        response = requests.request("GET", url, headers=headers, data=payload)

        DeleteGmail.processNextPageEmails(self,response.json())

    def trashGmailMails(self,mail_id):
        url = "https://gmail.googleapis.com/gmail/v1/users/{}/messages/{}/trash".format(self.user_id,mail_id)

        payload = {}
        headers = {'Authorization': 'Bearer {}'.format(self.bearer_token)}

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            print("\tEmail {} is trashed.".format(mail_id))

    def processGmailLable(self,json_lable):
        for dict_lable in json_lable["labels"]:
            if dict_lable["name"] == "Linkedin":
                delete_consent = input("\nDo you want to delete emails with lable {}?(y/n) : ".format(dict_lable["name"]))
                if delete_consent.lower() == 'y':
                    # Get Gmail Mail id with filter
                    json_lable_email_list = DeleteGmail.getGmailwithLableFilter(self,dict_lable["id"])

                    # Trash Email
                    for dict_lable_email_list in json_lable_email_list["messages"]:
                        DeleteGmail.trashGmailMails(self,dict_lable_email_list["id"])

                    # Get Next Page Emails
                    if json_lable_email_list["nextPageToken"]:
                        DeleteGmail.getNextPageGmailMails(self,json_lable_email_list["nextPageToken"])

                    print("\nEmails with lable {} are deleted".format(dict_lable["name"]))
                elif delete_consent.lower() == 'n':
                    print("\nEmails with lable {} are not deleted".format(dict_lable["name"]))
                else:
                    print("\nYou have entered a wrong input.")
                    break

    def processNextPageEmails(self,json_lable_email_list):
        for dict_lable_email_list in json_lable_email_list["messages"]:
            DeleteGmail.trashGmailMails(self, dict_lable_email_list["id"])

        if json_lable_email_list["nextPageToken"]:
            DeleteGmail.getNextPageGmailMails(self, json_lable_email_list["nextPageToken"])