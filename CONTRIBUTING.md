# Guia de Contribuição

Obrigado por dedicar seu tempo ao **README Generator**! Toda contribuição é bem-vinda — desde correções de typo até novas funcionalidades.

---

## Código de Conduta

Seja respeitoso e inclusivo em todas as interações. Críticas devem ser construtivas e focadas no código, não nas pessoas.

---

## Como Contribuir

### 1. Reportar Bugs

Antes de abrir uma issue, verifique se o problema já foi relatado. Se não, abra uma issue com:

- **Título** claro e descritivo
- **Passos para reproduzir** o problema
- **Comportamento esperado** vs. **comportamento atual**
- **Versão** do Python e do sistema operacional
- Logs de erro (se houver)

### 2. Sugerir Melhorias

Abra uma issue com a tag `enhancement` descrevendo:

- O problema que a melhoria resolve
- Como você imagina a solução
- Por que essa melhoria seria útil para outros usuários

### 3. Enviar Pull Requests

**Passo a passo:**

```bash
# 1. Faça um fork no GitHub e clone o seu fork
git clone https://github.com/seu-usuario/readme-generator.git
cd readme-generator

# 2. Crie uma branch descritiva a partir de main
git checkout -b feature/minha-nova-funcionalidade
# ou
git checkout -b fix/correcao-do-bug-xyz

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Faça as alterações e escreva os testes
# ... edite os arquivos ...

# 5. Execute os testes antes de commitar
pytest tests/ -v

# 6. Verifique o estilo do código
ruff check . --fix

# 7. Commit com mensagem seguindo o padrão Conventional Commits
git add .
git commit -m "feat: adiciona exportação do README em PDF"
# ou: fix: corrige erro 500 quando stack está vazia
# ou: docs: atualiza guia de instalação com Docker

# 8. Envie para o seu fork
git push origin feature/minha-nova-funcionalidade
```

Depois, abra um **Pull Request** no repositório original com:

- Descrição clara do que foi alterado
- Motivação para a mudança
- Como testar a alteração
- Screenshots (se a mudança for visual)

---

## Padrões do Projeto

### Commits (Conventional Commits)

| Prefixo | Quando usar |
|---|---|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `docs:` | Documentação |
| `test:` | Adição ou correção de testes |
| `refactor:` | Refatoração sem mudança de comportamento |
| `chore:` | Tarefas de manutenção (CI, deps, config) |

### Estilo de Código

- Python **3.11+** com type hints
- Formatação e lint via **Ruff** (`make lint`)
- Linhas com no máximo **100 caracteres**
- Docstrings não são obrigatórias, mas comentários devem explicar o **porquê**, não o **o quê**

### Testes

- Todo novo código deve vir acompanhado de testes
- Os testes ficam em `tests/` e devem usar `pytest` + `pytest-asyncio`
- Mocke chamadas externas — os testes não devem fazer requisições reais à API

---

## Dúvidas?

Abra uma [issue](https://github.com/jmello04/readme-generator/issues) com a tag `question`.
