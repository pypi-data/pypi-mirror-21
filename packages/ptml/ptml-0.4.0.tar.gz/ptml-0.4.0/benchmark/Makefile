

all:
	@echo
	@echo "***"
	@echo "***  Note: The benchmark currently only runs on UNIX platforms."
	@echo "***"
	@echo "***        The results will be stored in 'benchmark.html'"
	@echo "***"
	@echo
	@PYTHONPATH=`pwd`/..;	\
	export PYTHONPATH;	\
	python ../ptml/TemplateParser.py < ./benchmark.ptml | python

clean:
	rm -f cache/*.py cache/*.crc benchmark.html
