#this tool will take an iplist as requested by massscan and will make sure 
#the massscan process will stay up. the ip's will be split by this tool in smaller chunks
#and the tool will start massscan with the subprocess module making sure each cuhnk gets scanned until 
#the whole ip range at the beginning is done
#useful when you want to port scan huge IP ranges and you're too lazy to verify if the process failed


import subprocess
import optparse
import ipaddress
import datetime

NetworkRanges = []
#We Will create subranges of the ranges given and scan those. 
#we will use the subnetst() method from the ipaddress python module to divide networks in smaller chunks.
#/24 and smaller wont be divided. 
#/23 until /18 will be divided in two
#/smaller than /18 will be divided in 8 chunks

def GetOptions():
	parser = optparse.OptionParser()
	parser.add_option("--range", action="store",dest="ip", type="string")

	(options,args) = parser.parse_args()
	try:
        	IpRange= ipaddress.ip_network(options.ip)
	except ipaddress.AddressValueError:
        	print("[-] There is an error with your ip range")
	else:
        	print("[+] Stating splitting up the range "+str(IpRange))

	
	#getting network mask and setting up division for ranges
	#



	netmask1 = str(ipaddress.IPv4Network(IpRange))
	asd  = netmask1.split("/")
	netmask = int(asd[1])

	if (netmask >=24):
		NetworkRanges = list(IpRange.subnets())
		print(NetworkRanges)
	else:
		NetworkRanges = list(IpRange.subnets(new_prefix=23))
		print(NetworkRanges)


	return NetworkRanges


def ScanModule(xyz):
	
	for i in xyz:
		filename = str(i).split("/")[0]+"mask"+str(str(i).split("/")[1])+".txt"
		print(filename)
		x = 1
		while (x != 0):
			x = subprocess.check_call(["masscan","-oG",filename,"-p0-65535","--rate","1000000",str(i)])
	





if __name__=="__main__":
	asd = GetOptions()
	ScanModule(asd)
