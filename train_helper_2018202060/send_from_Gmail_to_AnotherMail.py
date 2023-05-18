import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import errors
from email.message import EmailMessage
import base64

def gmail_authenticate():
    SCOPES = ['https://mail.google.com/']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid: # token이 없는 경우
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('assets/client_secret_164017174304-4i4t2b22alheovdim2p0cb3n61pgkii1.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token: # token 생성
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text): # 메시지 생성
    message = EmailMessage()
    message["From"] = sender
    message["To"] = to
    message["Subject"] = subject
    message.set_content(message_text)
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf8')}

def send_message(service, user_id, message): #메시지 보내기
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def main(received_email):
    service = gmail_authenticate()
    f = open("assets/train_select.txt") #SRT인지 ktx인지 구별 후 결제창 보내기
    kind = f.readline()
    if kind == 'SRT':
        message = create_message("fakerlajbhc8406@naver.com", received_email, "SRT 예약완료", "예약을 결제하려면 https://etk.srail.kr/hpg/hra/02/selectReservationList.do?pageId=TK0102010000 에 접속하시길 바랍니다.")
    elif kind == 'KTX':
        message = create_message("fakerlajbhc8406@naver.com", received_email, "KTX 예약완료",
                                 "예약을 결제하려면 https://www.letskorail.com/ebizprd/EbizPrdTicketpr13500W_pr13510.do?1655642425498 에 접속하시길 바랍니다.")

    send_message(service, "me", message)
