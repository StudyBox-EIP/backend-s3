NAME	=	Camera 

SOURCE_FOLDER	=	src/

TEST_FOLDER	=	tests/

MAIN	=	$(SOURCE_FOLDER)__main__.py

RM	=	rm -fr

SYMLINK	=	ln -s

FORMATER	=	black

TEST	=	pytest -v --no-header

TYPE	=	mypy --pretty --strict --ignore-missing-imports --allow-untyped-globals

QUALITY	=	pylint -rn --fail-under=7.5

# Executes the program
all: clean
	pip install -r requirements.txt
	$(SYMLINK) $(MAIN) $(NAME)
	chmod +x $(NAME)

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

# Format every file with black
format:
	$(FORMATER) $(SOURCE_FOLDER)

.PHONY: all clean fclean re check_quality check_type tests_run assets format