# Python package makefile
#
# Uses git buildpackage, which from debian rules will call dh_virtualenv

test:
	tox

sdist:
	python setup.py sdist

clean:
	python setup.py clean
	debuild clean

deb:
	debuild -us -uc

changelog:
	gbp dch --ignore-branch --auto --commit debian

.PHONY: debian sdist test clean changelog
