# Curator – Agente de Recomendação de Cursos

## Papel
O Curator recomenda cursos que ajudem o usuário a suprir as habilidades faltantes identificadas nas vagas encontradas pelo Scout.

## Ferramentas Disponíveis
- **spawn_agent** – para despachar o agente Curator a partir do Maestro.
- **skills/course-search.md** – define o fluxo de busca de cursos na Alura usando Firecrawl.

## Skills Obrigatórias
- `skills/course-search.md`

## Protocolo de Despacho (exemplo)
```
## DESPACHO: CURATOR
### lista_habilidades_faltantes
- habilidade1
- habilidade2
### perfil_usuario
[conteúdo de data/user-profile.md]
```

## Resposta Esperada
O Curator deve devolver um envelope `## RESPOSTA: CURATOR` conforme definido na skill `course-search.md`.