# Plano de Aula 3 – Implementação do Agente Curator (Busca de Cursos)

## Objetivo da Aula
Desenvolver o agente **Curator**, responsável por buscar cursos na plataforma **alura.com.br** que complementem as habilidades faltantes do usuário em relação às vagas encontradas. O agente deve usar **Firecrawl** para navegar e extrair informações dos cursos, seguindo o mesmo padrão de fluxo adotado pelo agente **Scout**.

## Estrutura de Diretórios
```
agent-recruiter/
├─ personas/
│   ├─ scout.md          # já existente
│   └─ curator.md        # NOVO: Persona do agente Curator
├─ skills/
│   ├─ firecrawl.md      # existente
│   ├─ dispatch.md       # existente
│   ├─ course-search.md  # NOVO: Fluxo de busca de cursos na Alura
│   └─ job-search.md     # já existente (Scout)
├─ data/
│   ├─ user-profile.md   # existente
│   ├─ job-search-results.md  # existente (resultados do Scout)
│   └─ course-search-results.md  # NOVO: Últimos resultados do Curator
└─ plano-aula-3.md      # ESTE ARQUIVO
```

## 1️⃣ Criar a Skill `skills/course-search.md`
- **Ferramenta Zed**: `terminal` – executar comandos CLI do `firecrawl`.
- **Busca de Cursos**: `firecrawl search "cursos alura <skill>" --json` onde `<skill>` é cada habilidade faltante identificada nas vagas.
- **Detalhes do Curso**: `firecrawl scrape <url> --format markdown` para obter título, carga horária, nível, descrição e pré‑requisitos.
- **Correspondência de Habilidades**:
  - Para cada habilidade faltante, buscar cursos que a abordem.
  - Extrair a lista de tópicos/competências do curso (ex.: "O que você vai aprender").
  - Marcar como **coberto** se a habilidade aparecer nos tópicos.
- **Limite**: até **5 cursos** relevantes, priorizando aqueles que cobrem mais habilidades faltantes.
- **Formato de Resposta** esperado pelo Maestro (envelope com `estado`, `resumo`, `dados`, `erros`).
- **Tratamento de Erros**:
  - Falha no `firecrawl search` → registrar erro e abortar.
  - Falha no `firecrawl scrape` de um curso → usar título/descrição da busca e anotar a falha.
  - Caso não haja cursos para uma habilidade, pular e continuar com as demais.

## 2️⃣ Criar a Persona `personas/curator.md`
- **Papel**: Busca de cursos na Alura que preencham lacunas de competências.
- **Ferramentas Disponíveis**:
  - `terminal` (Firecrawl CLI).
  - `skills/course-search.md` (fluxo de busca de cursos).
  - `skills/firecrawl.md` (detalhes do CLI).
- **Skill Obrigatória**: `skills/course-search.md`.
- **Response Envelope**:
```
## RESPOSTA: CURATOR
### estado
- sucesso | erro
### resumo
- Texto curto descrevendo o que foi feito ou o erro encontrado.
### dados
- Lista de cursos (até 5) no formato definido em `course-search.md`.
### erros (opcional)
- Detalhes de falhas.
```
- **Regras de Erro** semelhantes ao Scout.

## 3️⃣ Atualizar o Maestro para despachar o Curator
- Quando o usuário escolher a opção **B** (Buscar cursos), o Maestro deve:
  1. Ler `data/job-search-results.md` para obter as **habilidades faltantes** das vagas.
  2. Montar o envelope de despacho para o Curator contendo:
     - Lista de habilidades faltantes.
     - Perfil do usuário (`data/user-profile.md`).
  3. Invocar `spawn_agent` com `label: "Curator - Busca de Cursos"` e o envelope como `message`.
  4. Receber a resposta, salvar em `data/course-search-results.md` e apresentar ao usuário.
  5. Retornar ao menu.
- Se `spawn_agent` falhar, comunicar erro e voltar ao menu.

## 4️⃣ Fallback de Acesso Web (opcional)
- Caso o `firecrawl search` falhe, usar `curl` para buscar a página de busca da Alura:
  ```
  curl -s "https://www.alura.com.br/busca?query=<skill>" | grep -i "curso"
  ```
- Extrair URLs dos cursos e seguir o mesmo fluxo de `scrape` (ou `curl` + parsing simples).
- Anotar no campo `erros` que o fallback foi utilizado.

## 5️⃣ Testes Manuais
1. **Cenário feliz** – Usuário escolhe B, Curator usa Firecrawl, devolve até 5 cursos que cobrem as habilidades faltantes.
2. **Falha do Firecrawl** – Simular erro; Curator recorre ao fallback `curl`, relata uso do fallback e ainda apresenta cursos.
3. **Nenhum curso encontrado** – Informar ao usuário e sugerir ampliar termos de busca.
4. **Erro de `spawn_agent`** – Maestro captura o erro e volta ao menu.

## Entregáveis da Aula
- `plano-aula-3.md` (este documento).
- `skills/course-search.md` – implementação completa do fluxo de busca de cursos.
- `personas/curator.md` – definição da persona e regras de operação.
- Atualização do Maestro para despachar o Curator conforme descrito.
- `data/course-search-results.md` – gerado dinamicamente após a primeira busca bem‑sucedida.

## Próximos Passos
- Validar a integração executando o fluxo completo no Zed.
- Caso tudo funcione, avançar para a implementação do agente **Coach** (simulação de entrevistas) conforme o roadmap.
