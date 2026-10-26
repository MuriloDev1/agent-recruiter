# Dispatch Skill

Esta skill define como o agente **Maestro** deve despachar outros agentes especializados usando a ferramenta `spawn_agent`.

## Uso
1. Construa um *envelope* contendo:
   - `## DESPACHO: <AGENTE>` – nome do agente a ser chamado (ex.: `SCOUT`).
   - `### referencia_persona` – conteúdo do arquivo de persona do agente.
   - `### tarefa` – descrição da tarefa a ser executada.
   - `### perfil_usuario` – informações do usuário armazenadas em `data/user-profile.md`.
   - `### contexto` – parâmetros adicionais (área, localização, nível, habilidades, etc.).
   - `### saida_esperada` – o formato esperado da resposta.
2. Chame a ferramenta:
   ```
   spawn_agent(label: "<AGENTE> - <Descrição>", message: "<envelope>")
   ```
3. Aguarde a resposta e trate os campos `estado`, `resumo` e `dados` conforme necessário.

## Exemplo de Envelope
```
## DESPACHO: SCOUT
### referencia_persona
[conteúdo de personas/scout.md]
### tarefa
Buscar vagas de emprego para {area} em {localizacao}
### perfil_usuario
[conteúdo de data/user-profile.md]
### contexto
Area: Desenvolvimento Web
Localizacao: São Paulo
Nivel: Pleno
Habilidades: JavaScript, React, Node.js
### saida_esperada
Envelope de resposta com estado, resumo, dados (lista de vagas) e erros se houver
```