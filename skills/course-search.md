# Course Search Skill (Curator)

## Overview
Esta skill define o fluxo que o agente **Curator** deve seguir para buscar cursos na Alura que preencham as habilidades faltantes do usuário.

## Ferramentas
- **terminal** – para executar os comandos CLI do `firecrawl`.
- **skills/firecrawl.md** – detalhes de uso do CLI (já existente).

## Entrada esperada
Um envelope de despacho contendo:
```
## DESPACHO: CURATOR
### lista_habilidades_faltantes
- habilidade1
- habilidade2
... 
### perfil_usuario
[conteúdo de data/user-profile.md]
```

## Fluxo de Execução
1. **Iterar sobre cada habilidade faltante** da lista recebida.
2. **Buscar cursos** na Alura usando Firecrawl:
   ```bash
   firecrawl search "cursos alura <habilidade>" --json
   ```
   - O comando retorna JSON com resultados contendo `url`, `title` e `description`.
3. **Selecionar até 5 cursos** que melhor correspondam às habilidades faltantes:
   - Para cada resultado, executar:
     ```bash
     firecrawl scrape <url> --format markdown
     ```
   - Extrair do markdown:
     - **Título** (primeira linha com `# `)
     - **Carga horária** (procure por padrão `Carga horária:`)
     - **Nível** (ex.: `Nível: Intermediário`)
     - **Descrição**
     - **Tópicos/competências** – seção típica "O que você vai aprender" ou lista de bullet points.
   - Verificar se a **habilidade** aparece nos tópicos. Marcar como coberta.
4. **Agrupar resultados**:
   - Cada curso deve conter:
     - `titulo`
     - `link`
     - `carga_horaria`
     - `nivel`
     - `habilidades_cobertas` (lista de habilidades que o curso aborda)
     - `habilidades_faltantes` (habilidades ainda não cobertas por nenhum curso selecionado)
   - Priorizar cursos que cubram **mais** habilidades faltantes.
5. **Limitar a 5 cursos** – interromper a iteração quando o limite for atingido.
6. **Construir Response Envelope**:
   ```markdown
   ## RESPOSTA: CURATOR
   ### estado
   - sucesso | erro
   ### resumo
   - Texto curto descrevendo o que foi feito ou o erro encontrado.
   ### dados
   - Lista de cursos no formato abaixo.
   ### erros (opcional)
   - Detalhes de falhas (ex.: falha no search ou scrape).
   ```
   **Formato de cada curso**:
   ```markdown
   1. titulo: <Título do Curso>
      link: <URL>
      carga_horaria: <horas>
      nivel: <Nível>
      habilidades_cobertas: [habilidade1, habilidade2]
      habilidades_faltantes: [habilidade3]
   ```
7. **Tratamento de Erros**
   - Se `firecrawl search` falhar para uma habilidade, registrar o erro em `erros` e continuar com as demais habilidades.
   - Se `firecrawl scrape` falhar para um URL, usar `title` e `description` retornados pela busca e anotar a falha.
   - Caso nenhuma habilidade resulte em cursos, retornar `estado: erro` com resumo indicando que não foram encontrados cursos.

## Fallback (opcional)
Se o comando `firecrawl search` falhar de forma geral, usar `curl` como fallback:
```bash
curl -s "https://www.alura.com.br/busca?query=<habilidade>" | grep -i "curso" | grep -oE 'href="[^"]+"' | head -n 5
```
Extrair URLs e seguir o mesmo fluxo de `scrape` (ou `curl` + parsing simples). Registrar no campo `erros` que o fallback foi utilizado.

## Saída
O agente Maestro deve salvar a resposta em `data/course-search-results.md` seguindo o mesmo padrão de `job-search-results.md`.
