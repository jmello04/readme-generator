.PHONY: install dev test test-cov lint format docker-up docker-down clean

## Instala as dependências do projeto
install:
	pip install -r requirements.txt

## Inicia o servidor em modo desenvolvimento (hot-reload)
dev:
	python main.py

## Executa a suite de testes
test:
	pytest tests/ -v --tb=short

## Executa os testes com relatório de cobertura
test-cov:
	pytest tests/ -v --tb=short --cov=app --cov-report=term-missing --cov-report=html

## Verifica e corrige problemas de estilo (ruff)
lint:
	ruff check . --fix

## Formata o código (ruff format)
format:
	ruff format .

## Sobe os containers Docker
docker-up:
	docker-compose up --build

## Para e remove os containers Docker
docker-down:
	docker-compose down

## Remove arquivos temporários e cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	@echo "✅  Limpeza concluída."
