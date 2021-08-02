from django.db import models
import googleapiclient
from google_auth_oauthlib import flow
from googleapiclient.discovery import build

google_api = None


class Chromebook(models.Model):
    serial_number = models.CharField(max_length=50)
    google_id = models.CharField(max_length=50)

    def __str__(self):
        return "Serial: " + str(self.serial_number) + " ID: " + str(self.google_id)


def update_chromebooks() -> str:
    print('updating chromebooks')
    # global google_api
    # if google_api is None:
    #     google_api = launch_google_auth()
    #     get_devices()
    # else:
    #     get_devices()

    return 'Success'


def launch_google_auth() -> googleapiclient.discovery.Resource:
    launch_browser = True
    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        "C:\Code\chromebooks\\files\desktop.json", scopes=["https://www.googleapis.com/auth/admin.directory.user",
        "https://www.googleapis.com/auth/admin.directory.device.chromeos",
        "https://www.googleapis.com/auth/admin.directory.group",
        "https://www.googleapis.com/auth/admin.directory.orgunit"])
    if launch_browser:
        appflow.run_local_server()
    else:
        appflow.run_console()

    creds = appflow.credentials
    return build('admin', 'directory_v1', credentials=creds)


def get_devices() -> str:
    next_page = 'na'

    while str(next_page) != "None":
        if next_page == 'na':
            devices = google_api.chromeosdevices().list(customerId='C02vc3t7l', orderBy='serialNumber', projection='BASIC', fields='chromeosdevices, nextPageToken').execute()
        else:
            devices = google_api.chromeosdevices().list(customerId='C02vc3t7l', orderBy='serialNumber', projection='BASIC', fields='chromeosdevices, nextPageToken', pageToken=next_page).execute()
        next_page = devices.get('nextPageToken')

        for device in devices.get('chromeosdevices'):
            device_id = device.get('deviceId')
            serial_num = device.get('serialNumber')
            new_book = Chromebook(serial_num, device_id)
            print(new_book)

    return 'Success'
