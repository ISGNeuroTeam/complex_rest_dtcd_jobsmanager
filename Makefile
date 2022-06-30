
#.SILENT:
SHELL = /bin/bash


all:
	echo -e "Required section:\n\
 build - build project into build directory, with configuration file and environment\n\
 clean - clean all addition file, build directory and output archive file\n\
 test - run all tests\n\
 pack - make output archive, file name format \"complex_rest_dtcd_jobsmanager_vX.Y.Z_BRANCHNAME.tar.gz\"\n\
Addition section:\n\
 venv\n\
"

GENERATE_VERSION = $(shell cat setup.py | grep __version__ | head -n 1 | sed -re 's/[^"]+//' | sed -re 's/"//g' )
GENERATE_BRANCH = $(shell git name-rev $$(git rev-parse HEAD) | cut -d\  -f2 | cut -d ^ -f1 | sed -re 's/^(remotes\/)?origin\///' | tr '/' '_')
SET_VERSION = $(eval VERSION=$(GENERATE_VERSION))
SET_BRANCH = $(eval BRANCH=$(GENERATE_BRANCH))

pack: make_build
	$(SET_VERSION)
	$(SET_BRANCH)
	rm -f complex_rest_dtcd_jobsmanager-*.tar.gz
	echo Create archive \"complex_rest_dtcd_jobsmanager-$(VERSION)-$(BRANCH).tar.gz\"
	cd make_build; tar czf ../complex_rest_dtcd_jobsmanager-$(VERSION)-$(BRANCH).tar.gz complex_rest_dtcd_jobsmanager --transform "s/^complex_rest_//"

clean_pack:
	rm -f complex_rest_dtcd_jobsmanager-*.tar.gz


complex_rest_dtcd_jobsmanager.tar.gz: build
	cd make_build; tar czf ../complex_rest_dtcd_jobsmanager.tar.gz complex_rest_dtcd_jobsmanager --transform "s/^complex_rest_//" && rm -rf ../make_build

build: make_build

make_build: venv.tar.gz
	# required section
	echo make_build
	mkdir make_build

	cp -R ./complex_rest_dtcd_jobsmanager make_build
	cp docs/jobsmanager_transit.conf.example make_build/complex_rest_dtcd_jobsmanager/jobsmanager_transit.conf
	cp docs/ot_simple_rest.conf.example make_build/complex_rest_dtcd_jobsmanager/ot_simple_rest.conf
	cp docs/proc.conf.example make_build/complex_rest_dtcd_jobsmanager/proc.conf
	cp *.md make_build/complex_rest_dtcd_jobsmanager/
	cp *.py make_build/complex_rest_dtcd_jobsmanager/
	mkdir make_build/complex_rest_dtcd_jobsmanager/venv
	tar -xzf ./venv.tar.gz -C make_build/complex_rest_dtcd_jobsmanager/venv
	rm -rf ./make_build/complex_rest_dtcd_jobsmanager/venv/lib/python3.9/site-packages/pathlib.py  # TODO figure out in future

clean_build:
	rm -rf make_build

venv:
	echo Create venv
	conda create --copy -p ./venv -y
	conda install -p ./venv python==3.9.7 -y
	./venv/bin/pip install --no-input  -r requirements.txt

venv.tar.gz: venv
	conda pack -p ./venv -o ./venv.tar.gz

clean_venv:
	rm -rf venv
	rm -f ./venv.tar.gz


complex_rest:
	@echo "Should clone complex_rest repository in future..."
# 	git clone git@github.com:ISGNeuroTeam/complex_rest.git
# 	{ cd ./complex_rest; git checkout develop; make venv; make redis; }
# 	ln -s ../../../../complex_rest_dtcd_jobsmanager/complex_rest_dtcd_jobsmanager ./complex_rest/complex_rest/plugins/complex_rest_dtcd_jobsmanager

clean_complex_rest:
ifneq (,$(wildcard ./complex_rest))
	{ cd ./complex_rest; make clean;}
	rm -f ./complex_rest/plugins/complex_rest_dtcd_jobsmanager
	rm -rf ./complex_rest
endif

clean: clean_build clean_venv clean_pack clean_test clean_complex_rest

test: venv complex_rest
	@echo "Testing..."
# 	./complex_rest/venv/bin/python ./complex_rest/complex_rest/manage.py test ./tests --settings=core.settings.test

clean_test: clean_complex_rest
	@echo "Clean tests"






