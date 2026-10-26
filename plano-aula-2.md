# Plano de Aula 2 – Implementação do Agente Scout (Busca de Vagas)

## Objetivo da Aula
Desenvolver o agente **Scout**, responsável por buscar vagas de emprego em sites como InfoJobs, Vagas.com e Indeed, utilizando a ferramenta **Firecrawl** via linha de comando. Caso o Firecrawl não esteja disponível, o agente deve recorrer à ferramenta de acesso web nativa (comando `curl`).

## Estrutura de Diretórios
```
agent-recruiter/
├─ personas/
│   └─ scout.md               # Persona do agente Scout (será criada)
├─ skills/
│   ├─ firecrawl.md           # Skill existente com detalhes de uso do CLI Firecrawl
│   ├─ dispatch.md            # Skill de despacho já criada
│   └─ job-search.md          # Skill que implementa o fluxo de busca de vagas (será criada)
├─ data/
│   ├─ user-profile.md        # Dados do usuário (já existente)
│   └─ job-search-results.md  # Resultado da última busca (será criado/atualizado)
└─ plano-aula-2.md            # Este documento
```

## Passos da Implementação

### 1️⃣ Criar a Skill `skills/job-search.md`
- Definir comandos **terminal** para executar `firecrawl search` e `firecrawl scrape`.
- Descrever como analisar o JSON retornado, extrair título, empresa, localização, link e requisitos.
- Implementar a lógica de correspondência entre as habilidades do usuário (arquivo `data/user-profile.md`) e as habilidades requeridas pela vaga.
- Incluir regras de filtragem por nível de experiência (Júnior, Pleno, Sênior) e limite de **até 5 vagas**.
- Definir o **formato de resposta** esperado pelo Maestro (envelope com `estado`, `resumo`, `dados` e `erros`).
- Documentar tratamento de falhas: erro na busca, erro na extração de detalhes, fallback para `curl`.

### 2️⃣ Criar a Persona `personas/scout.md`
- Descrever o papel do Scout e suas responsabilidades.
- Listar as ferramentas disponíveis: `terminal` (para Firecrawl) e, em caso de falha, `curl`/`wget` como fallback.
- Referenciar obrigatoriamente as skills `skills/job-search.md` e `skills/firecrawl.md`.
- Especificar o **Response Envelope** que o Scout deve devolver ao Maestro.
- Incluir regras de tratamento de erros (relatar no campo `erros` e não continuar silenciosamente).

### 3️⃣ Atualizar o Maestro para despachar o Scout
- No fluxo do menu, quando o usuário escolher a opção **A** (Buscar vagas), o Maestro deve:
  1. Ler `data/user-profile.md`.
  2. Montar o envelope de despacho conforme o modelo descrito em `agents.md`.
  3. Invocar `spawn_agent` com `label: "Scout - Busca de Vagas"` e o envelope como `message`.
  4. Receber a resposta, salvar em `data/job-search-results.md` e apresentar as vagas ao usuário.
  5. Retornar ao menu.
- Garantir que, se `spawn_agent` falhar, o erro seja comunicado ao usuário e o fluxo volte ao menu.

### 4️⃣ Implementar o Fallback de Acesso Web
- Dentro da skill `job-search.md`, após uma falha do comando `firecrawl search`, executar:
  ```
  curl -s "https://www.google.com/search?q=vagas+<area>+<localizacao>" | grep -i "indeed\|infojobs\|vagas.com"
  ```
- Parsear rapidamente os resultados (título e URL) e seguir o mesmo fluxo de extração de requisitos usando `curl` ou `wget` para obter o HTML da vaga.
- Avisar ao usuário que o fallback foi utilizado e que a qualidade da extração pode ser reduzida.

### 5️⃣ Testes Manuais
1. **Cenário feliz** – Usuário escolhe A, Scout executa `firecrawl`, devolve 5 vagas com correspondência de habilidades.
2. **Falha do Firecrawl** – Simular erro (por exemplo, removendo a variável de ambiente). O Scout deve usar o fallback `curl`, relatar o uso do fallback e ainda apresentar vagas.
3. **Nenhum resultado** – Quando a busca não retorna vagas, o Scout deve informar ao usuário e sugerir ampliar os termos.
4. **Erro de `spawn_agent`** – Verificar que o Maestro captura o erro e volta ao menu.

## Entregáveis da Aula
- `plano-aula-2.md` (este documento).
- `skills/job-search.md` – implementação completa do fluxo de busca.
- `personas/scout.md` – definição da persona e regras de operação.
- Atualização do Maestro (arquivo de skill ou lógica) para despachar o Scout conforme descrito.
- `data/job-search-results.md` – gerado dinamicamente após a primeira busca bem‑sucedida.

## Próximos Passos
- Após concluir a aula, validar a integração executando o fluxo completo no Zed.
- Caso tudo funcione, avançar para a próxima extensão (Curator ou Coach) conforme o roadmap.
