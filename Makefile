PKG = kord

DISTR_DIRS = dist \
		build \
		${PKG}.egg-info

CLEAN_DIRS = kord/__pycache__ \
		kord/keys/__pycache__ \
		kord/notes/__pycache__ \
		kord/notes/constants/__pycache__ \
		kord/parsers/__pycache__ \
		app/__pycache__


default: build install clean

get_version: setup.py
	@$(eval VER := $(shell cat setup.py | grep version | cut -d'=' -f 2 | cut -d',' -f 1))

build: get_version setup.py ${PKG}
	@python3 setup.py sdist bdist_wheel && echo "done building ${PKG} ${VER}, bye!" || exit

install: get_version ${DISTR_DIRS}
	@echo "Installing ${PKG} ${VER}"
	@cd dist && \
	source ~/.pyenv/versions/"${PKG}"/bin/activate \
	&& pip  install --ignore-installed "${PKG}"-"${VER}"-py3-none-any.whl \
	|| pip3 install --ignore-installed "${PKG}"-"${VER}"-py3-none-any.whl

clean:
	-@for dir in ${DISTR_DIRS} ; do \
		[ -d "$${dir}" ] && rm -rf "$${dir}" && echo "Deleted dir:  $${dir}" \ ; \
	done
	-@for dir in ${CLEAN_DIRS} ; do \
		[ -d "$${dir}" ] && rm -rf "$${dir}" && echo "Deleted dir:  $${dir}" \ ; \
	done

publish: build
	@echo "Uploading to pypi.org/project/"${PKG}"/ >>>"
	@twine upload dist/*

run:
	@source ~/.pyenv/versions/"${PKG}"/bin/activate \
	&& python  app/fretboard.py  C  -f9

test:
	@source ~/.pyenv/versions/"${PKG}"/bin/activate \
	&& python  test.py \
	|| python3 test.py

dev:
	@source ~/.pyenv/versions/"${PKG}"/bin/activate \
	&& python  dev.py \
	|| python3 dev.py
