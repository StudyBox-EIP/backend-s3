NAME	=	Camera 

MAIN	=	src/__main__.py

RM	=	rm -fr

# Executes the program
all: clean
	pip install -r requirements.txt
	ln -s $(MAIN) $(NAME)
	chmod +x $(NAME)

# Remove Binary
clean:
	$(RM) $(NAME)

# Remove Temp Files & Binary
fclean: clean
	$(RM) .mypy_cache
	$(RM) .pytest_cache
	$(RM) **/**/__pycache__

# Downaload dependency & makes binary after fclean
re: fclean all

# Checks code quality with pylint
quality:
	pylint -rn src/

# Generates a badge for code
badge:
	pylint-badge src docs/pylint.svg

# Checks errors and code quality with mypy
check:
	mypy --strict --ignore-missing-imports src

# Runs all the tests
tests_run:
	pytest tests

# Format every file with black
format:
	black .

.PHONY: all clean fclean re quality badge check tests_run format