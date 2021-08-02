from django.core.management.base import BaseCommand, CommandError
import googleapiclient
from google_auth_oauthlib import flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--fromfile',
            action='store_true',
            help='Moves Chromebooks from a CSV list of serial numbers',
        )
        parser.add_argument('file_path', help='Full File Path with file extension')

    def handle(self, *args, **options):
        if options['fromfile']:
            self.enable_chromebooks(options['file_path'])

    def move_to_student_deployable(self, file_path):
        with open(file_path) as csv:
            serials = csv.read().splitlines()

        google_creds = self.get_google_creds()
        chromebooks = self.get_chromebooks(google_creds)

    def enable_chromebooks(self, file_path):
        with open(file_path) as csv:
            serials = csv.read().splitlines()

        google_creds = self.get_google_creds()
        chromebooks = self.get_chromebooks(google_creds)

        for serial in serials:
            serial = serial.upper()

            if serial in chromebooks.keys():
                google_device_id = chromebooks[serial]
                try:
                    google_creds.chromeosdevices().moveDevicesToOu(
                        customerId='C02vc3t7l',
                        orgUnitPath='/Devices/Chromebooks/Student Deployable',
                        body={"deviceIds": [google_device_id]}).execute()
                    print('Moved serial:', serial, google_device_id)

                except HttpError as error:
                    message = error.error_details[0]['message']
                    print(serial, 'HTTP error:', message)
            else:
                print(serial, 'not found in Google Workspace')

    #        C:\Users\ianwa\Downloads\books.csv

    def get_google_creds(self) -> googleapiclient.discovery.Resource:
        launch_browser = True
        appflow = flow.InstalledAppFlow.from_client_secrets_file(
            "C:\Code\chromebooks\\files\desktop.json",
            scopes=["https://www.googleapis.com/auth/admin.directory.user",
                    "https://www.googleapis.com/auth/admin.directory.device.chromeos",
                    "https://www.googleapis.com/auth/admin.directory.group",
                    "https://www.googleapis.com/auth/admin.directory.orgunit"])
        if launch_browser:
            appflow.run_local_server()
        else:
            appflow.run_console()

        creds = appflow.credentials
        return build('admin', 'directory_v1', credentials=creds)

    def get_chromebooks(self, google_api) -> dict:
        next_page = 'na'
        chromebooks = {}

        while str(next_page) != "None":
            if next_page == 'na':
                devices = google_api.chromeosdevices().list(customerId='C02vc3t7l', orderBy='serialNumber',
                                                            projection='BASIC', orgUnitPath='/Devices/Chromebooks/Student Deployable',
                                                            fields='chromeosdevices, nextPageToken').execute()
            else:
                devices = google_api.chromeosdevices().list(customerId='C02vc3t7l', orderBy='serialNumber',
                                                            orgUnitPath='/Devices/Chromebooks/Student Deployable',
                                                            projection='BASIC', fields='chromeosdevices, nextPageToken',
                                                            pageToken=next_page).execute()
            next_page = devices.get('nextPageToken')

            for device in devices.get('chromeosdevices'):
                device_id = device.get('deviceId')
                serial_num = device.get('serialNumber')
                chromebooks[serial_num] = device_id

        return chromebooks

