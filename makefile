source_dir = src
virtualenv = .venv
app_module = main:app

run:
	cd $(source_dir) && uvicorn $(app_module) --reload

up:
	@docker compose down
	@docker compose up --build

cleanup:
	@find . -type d \( -path "./$(virtualenv)" -o -path "./.data" \) -prune -o -type d -name '*cache*' \
	-exec echo Removing {} \; \
	-exec rm -rf {} +

tree:
	@tree -a -I "$(virtualenv)|.git|.data|__pycache__"

pre-commit:
	git add .
	@pre-commit run -a

commit-and-push:
	@read -p "Enter commit message: " message; \
	git add .; \
	git commit -m "$$message"; \
	git push -u origin `git rev-parse --abbrev-ref HEAD`
