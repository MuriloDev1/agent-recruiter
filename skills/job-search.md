# Job Search Skill

## Overview
This skill defines the complete flow for the **Scout** agent to search for job vacancies using **Firecrawl** (CLI) and, if necessary, fallback to `curl`. It processes the JSON results, scrapes detailed job pages, matches required skills against the user's profile, filters by experience level, and formats the response envelope expected by the Maestro.

## Prerequisites
- `firecrawl` CLI installed and authenticated (`FIRECRAWL_API_KEY` set).
- Access to `data/user-profile.md` for the user's current skills, desired area, location and experience level.

## Tools
- **terminal** – to run `firecrawl search`, `firecrawl scrape` and optionally `curl`.
- **read_file** – to read `data/user-profile.md`.
- **write_file** – to store intermediate data if needed (not required for the core flow).

## Step‑by‑Step Flow
1. **Load user profile**
   ```
   read_file(path="data/user-profile.md")
   ```
   Extract the following fields (case‑insensitive):
   - `area_de_interesse`
   - `localizacao`
   - `nivel_experiencia` (Júnior, Pleno, Sênior)
   - `habilidades` – a comma‑separated list.

2. **Build the search query**
   ```
   query = f"vagas {area_de_interesse} {localizacao}"
   ```
   The query is passed directly to `firecrawl search`.

3. **Execute primary search**
   ```
   firecrawl search "{query}" --json
   ```
   The command returns a JSON array where each element contains at least:
   - `url`
   - `title`
   - `description`
   - `metadata` (may contain `company`, `location`).

   If the command exits with a non‑zero status, **fallback** to step 4.

4. **Fallback search (curl)**
   ```
   curl -s "https://www.google.com/search?q=vagas+{area_de_interesse}+{localizacao}" | grep -iE "indeed|infojobs|vagas.com|linkedin"
   ```
   Parse the output for URLs (simple regex) and build a list of candidate URLs. This fallback provides only URLs; title and description are taken from the Google snippet when available.

5. **Select up to 5 candidate URLs**
   - Keep the order returned by the primary search; if fallback is used, keep the order of appearance.
   - Stop after 5 URLs.

6. **Scrape each candidate**
   For each URL:
   ```
   firecrawl scrape {url} --format markdown
   ```
   - If the scrape succeeds, keep the full markdown description.
   - If it fails, **fallback** to a lightweight `curl` request:
     ```
     curl -s {url}
     ```
     Use the raw HTML title/description as a best‑effort fallback and note the failure in the `erros` field.

7. **Extract required skills**
   - Look for a section titled *Requisitos*, *Requirements*, *Skills* or a bullet list.
   - Use a simple regex to capture words that look like skills (e.g., `\b[A-Za-z+]+\b`).
   - Normalize to lower case and deduplicate.

8. **Match against user skills**
   - `habilidades_correspondentes` = intersection of required skills and user skills.
   - `habilidades_faltantes` = required skills minus user skills.
   - `contagem_correspondencia` = "X de Y habilidades correspondem" where X = |correspondentes| and Y = |required|.

9. **Filter by experience level**
   - Scan the job description for the words `junior`, `pleno`, `senior` (case‑insensitive).
   - Keep only jobs whose level matches the user's `nivel_experiencia`.
   - If fewer than 5 matches are found, relax the filter to include adjacent levels (e.g., a Júnior user may also see Pleno positions, marked with a note).

10. **Build the response envelope**
    ```json
    {
      "estado": "sucesso" | "erro",
      "resumo": "<human readable summary>",
      "dados": [
        {
          "titulo": "...",
          "empresa": "...",
          "localizacao": "...",
          "link": "...",
          "habilidades_correspondentes": ["..."],
          "habilidades_faltantes": ["..."],
          "contagem_correspondencia": "X de Y habilidades correspondem"
        }
        // up to 5 items
      ],
      "erros": []
    }
    ```
    - If any step fails (search, scrape, parsing), add a descriptive string to `erros` and set `estado` to `erro` only if **no** job could be produced. Partial failures keep `estado: "sucesso"` with the jobs that succeeded and list the errors.

## Error Handling Rules
- **Search failure** → use fallback `curl`. If fallback also fails, return `estado: "erro"` with a clear message.
- **Scrape failure for a specific URL** → use the title/description from the search result, add an entry to `erros` like `"Scrape failed for {url}: {error_message}"` and continue.
- **Skill extraction failure** → treat the job as having zero required skills; match count will be `0 de 0` and the job will still be listed.
- **Unexpected JSON structure** → log the raw output in `erros` and skip that entry.

## Expected Output Example
```
## RESPOSTA: SCOUT
estado: sucesso
resumo: Encontradas 3 vagas que correspondem ao seu perfil.
erros: []

dados:
1. titulo: Engenheiro Frontend
   empresa: TechCorp
   localizacao: São Paulo (Remoto)
   link: https://www.indeed.com/viewjob?jk=12345
   habilidades_correspondentes: [react, javascript, css]
   habilidades_faltantes: [typescript]
   contagem_correspondencia: 3 de 4 habilidades correspondem

2. titulo: Desenvolvedor Full‑Stack
   empresa: InovaSoft
   localizacao: Rio de Janeiro
   link: https://www.infojobs.com.br/vaga/67890
   habilidades_correspondentes: [nodejs, docker]
   habilidades_faltantes: [kubernetes, aws]
   contagem_correspondencia: 2 de 4 habilidades correspondem
```

---
*This file is consumed by the Scout persona (see `personas/scout.md`).*