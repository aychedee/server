.PHONY: deploy
deploy:
	ansible-playbook deploy/site.yml 

vpn:
	ansible-playbook deploy/vpn.yml 

clean:
	rm -rf www.aychedee.com/_build

deploy-aychedee:
	ansible-playbook deploy/site.yml --tags aychedee

deploy-interpretthis:
	ansible-playbook deploy/site.yml --tags interpretthis

aychedee.com:
	run-rstblog build www.aychedee.com/

