import os, sys
from flask import Flask, request
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAe37AxDgHsBAOG8U0m1G1UwOFb7TSTbLjfS19RAWUXqZC6otHgKk14ATvZBoaQNjqTsqgiFwRFBuOQyZB4NULlkiBZCbQSMASeAtEKOeUZCGaGCc6nWWbC9V00cBZAeAPXfAnR5elm8f1HWz8mrZCAZBSCpeZASZA6XRL5Tm5qvinfQZDZD"
bot = Bot(PAGE_ACCESS_TOKEN)

VERIFICATION_TOKEN = "thaiminh"

@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
	print(request.data)
	data = request.get_json()
	log(data)

	if data['object'] == "page":
		entries = data['entry']

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:

				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# HANDLE NORMAL MESSAGES HERE
					if messaging_event['message'].get('text'):
						# HANDLE TEXT MESSAGES
						query = messaging_event['message']['text'] + " Nguyen Thai Minh"
						# ECHO THE RECEIVED MESSAGE
						bot.send_text_message(sender_id, query)

	return "Hello World", 200

def log(message):
	print(message)
	sys.stdout.flush()

if __name__ == "__main__":
	app.run(port=8000, use_reloader=True)

# from bs4 import BeautifulSoup
# import urllib.request
# import requests
# import pandas as pd
#
# # Request to http://sv.dut.udn.vn
# url = 'http://sv.dut.udn.vn/'
# page = urllib.request.urlopen(url)
#
# # Using BeautifulSoup analysis HTML
# soup = BeautifulSoup(page, 'html.parser')
#
# # Retrieve content from notification from http://sv.dut.udn.vn
# posts_date = soup.find_all('div', class_='tbBoxCaption', limit=5)
# content = soup.find_all('div', class_='tbBoxContent', limit=5)
#
# # for i in range(5):
# #     print('Thông báo ngày:', posts_date[i].text)
# #     print(content[i].text)
# #     print('------------------------')
#
# url_login = 'http://sv.dut.udn.vn/PageDangNhap.aspx'
# url_gpa = 'http://sv.dut.udn.vn/PageKQRL.aspx'
# url_schedule = 'http://sv.dut.udn.vn/PageLichTH.aspx'
#
# header ={
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
# }
#
# login_data = {
#     'ctl00$MainContent$DN_txtAcc': '102160218',
#     'ctl00$MainContent$DN_txtPass': 'minhmui2110',
#     'ctl00$MainContent$QLTH_btnLogin': 'Đăng nhập'
# }
#
# with requests.Session() as s:
#     response = s.get(url_login, headers=header)
#
#     soup_key = BeautifulSoup(response.content, 'html.parser')
#     soup_key1 = BeautifulSoup(response.content, 'html.parser')
#
#     login_data['__VIEWSTATEGENERATOR'] = soup_key.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']
#     login_data['__VIEWSTATE'] = soup_key1.find('input', attrs={'name': '__VIEWSTATE'})['value']
#
#     requests = s.post(url_login, data=login_data, headers=header)
#
#     schedule_request = s.get(url_schedule)
#     get_gpa_request = s.get(url_gpa)
#
#     soup_information = BeautifulSoup(requests.text, 'html.parser')
#     soup_gpa_request = BeautifulSoup(get_gpa_request.text, 'html.parser')
#     gpa_table = soup_gpa_request.find('table', attrs={'id': 'KQRLGridTH'})
#     rows_gpa_table = gpa_table.find_all('td')
#
#     student_faculty = soup_information.find('input', attrs={'name': 'ctl00$MainContent$CN_txtNganh'})['value']
#     name_student = soup_information.find('input', attrs={'name': 'ctl00$MainContent$CN_txtHoTen'})['value']
#     student_class = soup_information.find('input', attrs={'name': 'ctl00$MainContent$CN_txtLop'})['value']
#     phone_number = soup_information.find('input', attrs={'name': 'ctl00$MainContent$CN_txtPhone'})['value']
#
#     print('Khoa:', student_faculty)
#     print('Họ và tên sinh viên:', name_student.upper())
#     print('Lớp:', student_class)
#     print('Số điện thoại:', phone_number)
#
#     print('Điểm Trung bình cộng tích lũy thang 4:', rows_gpa_table[-14].text)
#     print('Số tín chỉ tích lũy:', rows_gpa_table[-15].text)
#
#     soup_schedule = BeautifulSoup(schedule_request.text, 'html.parser')
#     table = soup_schedule.find('table', attrs={'id': 'TTKB_GridInfo'})
#     print(table.text)
#
#     rows = table.find_all('td')
#
#     total_subjects = int(len(rows)/14)
#     count = 0
#
#     id = []
#     class_codes = []
#     class_names = []
#     subject_credits = []
#     lecturers = []
#     schedules = []
#     school_week = []
#
#     while count < total_subjects:
#         id.append(rows[0 + 14*count].text.strip())
#         class_codes.append(rows[1 + 14*count].text.strip())
#         class_names.append(rows[2 + 14*count].text.strip())
#         subject_credits.append(rows[3 + 14*count].text.strip())
#         lecturers.append(rows[6 + 14*count].text.strip())
#         schedules.append(rows[7 + 14*count].text.strip())
#         school_week.append(rows[8 + 14*count].text.strip())
#         count += 1
#
#     schedule_dictionary = {
#                            'Mã lớp học phần': class_codes,
#                            'Tên lớp học phần': class_names,
#                            'Số tín chỉ': subject_credits,
#                            'Giảng viên': lecturers,
#                            'Thời khóa biểu': schedules,
#                            'Tuần học': school_week}
#
#     # sum_credits = 0
#     # for element in subject_credits:
#     #     sum_credits += int(element)
#     #
#     # print(sum_credits)
#
#     schedule_df = pd.DataFrame(schedule_dictionary, index=id)
#     print(schedule_df)