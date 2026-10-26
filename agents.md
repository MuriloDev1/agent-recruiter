# Agents Overview

Este documento descreve os agentes que compõem o sistema **Orquestrador de Vagas Tech**.

## Maestro (Orquestrador)
- **Responsabilidade**: interface principal com o usuário, gerenciamento de fluxo, delegação de tarefas a agentes especializados.
- **Skills**: `skills/dispatch.md` (despacho de agentes), `skills/quiz-management.md` (gerenciar quiz de habilidades), `skills/menu.md` (exibir opções ao usuário).
- **Persona**: `personas/maestro.md` (a ser criada).

## Scout (Busca de Vagas)
- **Responsabilidade**: buscar vagas de emprego usando Firecrawl, analisar requisitos e devolver até 5 vagas relevantes.
- **Skill**: `skills/job-search.md`.
- **Persona**: `personas/scout.md`.

## Futuras Extensões
- **Curator** – agente de recomendação de cursos.
- **Coach** – agente de simulação de entrevistas.
