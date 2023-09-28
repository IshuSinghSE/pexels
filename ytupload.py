
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "Description of uploaded video.",
                "title": "Test video upload."
            },
            "status": {
                # "privacyStatus": "private",
                "publistAt": "2023-09-28T10:00+05:30"
            }
        },

        media_body=MediaFileUpload("output.mp4", resumable=True)
    )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    print(os.listdir())
    main()
