NAME	=	Camera 

SOURCE_FOLDER	=	src/Software/

TEST_FOLDER	=	tests/

MAIN	=	$(SOURCE_FOLDER)main.py

RM	=	rm -fr

SYMLINK	=	ln -s

FORMATER	=	black

TEST	=	pytest -v --no-header

TYPE	=	mypy --pretty --strict --ignore-missing-imports --allow-untyped-globals

QUALITY	=	pylint -rn --fail-under=7.5

# Executes the program
all: install clean
	$(SYMLINK) $(MAIN) $(NAME)
	chmod +x $(NAME)

install:
	pip install -r requirements.txt

# Remove Binary
clean:
	$(RM) $(NAME)

# Remove Temp Files & Binary
fclean: clean
	$(RM) .mypy_cache
	$(RM) .pytest_cache
	$(RM) **/**/__pycache__
	$(RM) *.json
	$(RM) *.csv

# Downaload dependency & makes binary after fclean
re: fclean all

# Checks code quality with pylint
check_quality:
	$(QUALITY) $(SOURCE_FOLDER)

# Checks errors and code quality with mypy
check_type:
	$(TYPE) $(SOURCE_FOLDER)

# Runs all the tests
tests_run:
	$(TEST) $(TEST_FOLDER)

# Download assets
assets:
	./download.sh

remove_typing:
	echo y | pip uninstall typing

# Make executable files
executable:	install remove_typing
	pyinstaller --onefile src/Configuration/main.py
	mv dist/main ./Configuration.exe

# Format every file with black
format:
	$(FORMATER) $(SOURCE_FOLDER)

.PHONY: all clean fclean re check_quality check_type tests_run assets format remove_typing executable
