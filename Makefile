PACKAGE = kord
DISTR_DIRS = dist   build   ${PACKAGE}.egg-info
CLEAN_DIRS = kord/__pycache__/ kord/keys/__pycache__/ kord/notes/__pycache__/ kord/notes/constants/__pycache__/ kord/parsers/__pycache__/

default: build install clean

get_version: setup.py
	@$(eval VERSION := $(shell cat setup.py | grep version | cut -d'=' -f 2 | cut -d',' -f 1))

build: get_version setup.py ${PACKAGE}
	@echo "Building ${PACKAGE} ${VERSION}..."
	@python3 setup.py sdist bdist_wheel && echo "Success" || exit

install: get_version ${DISTR_DIRS}
	@echo "Installing ${PACKAGE} ${VERSION}"
	@cd dist && pip3 install --ignore-installed "${PACKAGE}"-"${VERSION}"-py3-none-any.whl && cd ..

clean:
	@echo "Cleaning up"
	-@for dir in ${DISTR_DIRS} ; do \
		[ -d "$${dir}" ] && rm -rf "$${dir}" && echo "Deleted $${dir} directory" \ ; \
	done
	-@for dir in ${CLEAN_DIRS} ; do \
		[ -d "$${dir}" ] && rm -rf "$${dir}" && echo "Deleted $${dir} directory" \ ; \
	done

publish: build
	@echo "Uploading to PyPI "
	@twine upload dist/*

test:
	@source ~/.pyenv/versions/"${PACKAGE}"/bin/activate && python test.py || python3 test.py

dev:
	@source ~/.pyenv/versions/"${PACKAGE}"/bin/activate && python dev.py  || python3 dev.py
