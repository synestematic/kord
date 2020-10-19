PACKAGE = kord
DISTR_DIRS = dist build ${PACKAGE}.egg-info

default: build install clean

upload: build install publish clean

get_version: setup.py
	@$(eval VERSION := $(shell cat setup.py | grep version | cut -d'=' -f 2 | cut -d',' -f 1))

build: get_version setup.py ${PACKAGE}
	@echo "Building ${PACKAGE} ${VERSION}..."
	@python3 setup.py sdist bdist_wheel && echo "Success" || exit

install: get_version ${DISTR_DIRS}
	@echo "Installing ${PACKAGE} ${VERSION}"
	@cd dist && pip3 install --ignore-installed "${PACKAGE}"-"${VERSION}"-py3-none-any.whl && cd ..

publish: dist
	@echo "Uploading to PyPI "
	@twine upload dist/*

clean: ${DISTR_DIRS}
	@echo "Cleaning up"
	@for dir in ${DISTR_DIRS} ; do \
		[ -d "$${dir}" ] && rm -rf "$${dir}" && echo "Deleted $${dir} directory" \ ; \
	done
