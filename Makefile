NAME	=	Camera 

all:
	pip install -r requirement.txt
	ln -s src/main.py $(NAME)
	chmod +x $(NAME)

clean:
	rm -f $(NAME)

fclean: clean
	rm -fr .mypy_cache
	rm -fr */__pycache__

re: fclean all

check:
	mypy --strict --ignore-missing-imports src

tests_run:
	pytest tests

format:
	black .

.PHONY: all format check tests_run clean fclean re