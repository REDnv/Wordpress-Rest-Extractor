#!/usr/bin/python3
import requests, urllib3, os, json, argparse
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def mediascan(host,scantype,perpage,page):
	# Date
	now = datetime.now()
	dt = now.strftime("%d-%m-%Y %H:%M:%S")
	print("[%s+%s] %sWordPress Rest Extractor%s by: Vanderlei Oliveira %s@REDnv%s"%(bcolors.OKGREEN,bcolors.ENDC,bcolors.OKGREEN,bcolors.ENDC,bcolors.FAIL,bcolors.ENDC))
	print("[%s+%s] Starting at %s"%(bcolors.OKGREEN,bcolors.ENDC,dt))
	
	# Check the type of scan to show the amount of users or medias
	if(scantype == 1):
		hostfinal = (host+"wp-json/wp/v2/media?per_page=%i&page=%i"%(perpage,page))
		stype = "Medias"
	elif(scantype == 2):
		hostfinal = (host+"wp-json/wp/v2/users?per_page=%i&page=%i"%(perpage,page))
		stype = "Users" 
	else:
		print("Error")
		
	# Request to get total of objects and total of pages
	r = requests.get(url=hostfinal, verify=False)
	totalobjects = int(r.headers['x-wp-total'])
	totalpages = int(r.headers['x-wp-totalpages'])

	print("[%s+%s] Total of %s: %s%s%s"%(bcolors.OKGREEN,bcolors.ENDC,stype,bcolors.OKGREEN,totalobjects,bcolors.ENDC))
	print("[%s+%s] Total of Pages: %s%s%s\n"%(bcolors.OKGREEN,bcolors.ENDC,bcolors.OKGREEN,totalpages,bcolors.ENDC))

	while (page <= totalpages):
		if(scantype == 1):
			hostfinal = (host+"wp-json/wp/v2/media?per_page=%i&page=%i"%(perpage,page))
		elif(scantype == 2):
			hostfinal = (host+"wp-json/wp/v2/users?per_page=%i&page=%i"%(perpage,page))
		else:
			print("Error")
		r = requests.get(url=hostfinal, verify=False)
		r.raise_for_status()
		jsonResponse = r.json()
		count=0
		toip = len(r.json()) # total of objects in a page
		while (count < toip):
			# Realtime Date
			now = datetime.now()
			dt = now.strftime("%H:%M:%S")
			if(scantype == 1):
				sourceurl = jsonResponse[count]['source_url']
				print("[%s%s%s] %s"%(bcolors.OKGREEN,dt,bcolors.ENDC,sourceurl))
				# Append in a file.
				f=open("wp-medias.txt", "a+")
				f.write(sourceurl + "\n")
			elif(scantype == 2):
				users = jsonResponse[count]['slug']
				print("[%s%s%s] %s"%(bcolors.OKGREEN,dt,bcolors.ENDC,users))
				# Append in a file.
				f=open("wp-users.txt", "a+")
				f.write(users + "\n")
			count+=1
		print("\n[%s+%s] Page: %i"%(bcolors.OKGREEN,bcolors.ENDC,page)) #Debug Page
		page+=1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wordpress Users and Media scans')
    requiredNamed = parser.add_argument_group('required named arguments')
    parser.add_argument('-t', '--target', required=True, dest='target', type=str)
    parser.add_argument('-u', '--users', help='scan for users', dest='users', action='store_true')
    parser.add_argument('-m', '--media', help='scan for media attachments', dest='media', action='store_true')
    parser.add_argument('-p', '--perpage', required=True, help='number of objects for page', dest='perpage', type=int)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()
    page=1  # by default page starts at 1
    
    target = args.target
    
    if target[len(target)-1] != "/":
        target = target + "/"
        
    if args.media:
        scantype = 1
        mediascan(target,scantype,args.perpage,page)
    elif args.users:
        scantype = 2
        mediascan(target,scantype,args.perpage,page)
    else:
        import sys
        print(f'Usage help: python {sys.argv[0]} -h')
