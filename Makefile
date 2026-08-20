produce:
	git pull
	curl -o china_ip_list.txt https://raw.githubusercontent.com/mayaxcn/china-ip-list/refs/heads/master/chnroute.txt
	python3 update.py
	cat update.txt | vtysh