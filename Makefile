NAME	=	Camera 

MAIN	=	src/__main__.py

RM	=	rm -fr

all: clean
	pip install -r requirements.txt
	ln -s $(MAIN) $(NAME)
	chmod +x $(NAME)

clean:
	$(RM) $(NAME)

fclean: clean
	$(RM) .mypy_cache
	$(RM) .pytest_cache
	$(RM) */__pycache__

re: fclean all

check:
	mypy --strict --ignore-missing-imports src

tests_run:
	pytest tests

format:
	black .

.PHONY: all clean fclean re check tests_run format