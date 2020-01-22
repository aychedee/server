.PHONY: deploy
deploy:
	ansible-playbook -i inventory.ini deploy/site.yml 

vpn:
	ansible-playbook -i inventory.ini deploy/vpn.yml 

clean:
	rm -rf www.aychedee.com/_build

deploy-aychedee:
	ansible-playbook -i inventory.ini deploy/site.yml --tags aychedee

deploy-interpretthis:
	ansible-playbook -i inventory.ini deploy/site.yml --tags interpretthis

aychedee.com:
	run-rstblog build www.aychedee.com/

