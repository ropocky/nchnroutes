produce:
	git pull
#	curl -o china_ip_list.txt https://raw.githubusercontent.com/mayaxcn/china-ip-list/refs/heads/master/chnroute.txt
	curl -o china_ip_list.txt https://gaoyifan.github.io/china-operator-ip/china.txt
	python3 update.py
	cat update.txt | vtysh