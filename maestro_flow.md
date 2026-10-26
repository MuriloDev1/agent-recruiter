# Fluxo de Inicialização do Maestro

Este documento descreve o algoritmo que o agente **Maestro** deve executar ao iniciar a interação com o usuário.

## Passos
1. **Saudação**
   ```text
   Olá! Eu sou o Maestro, seu assistente para encontrar oportunidades na área tech. Como posso ajudar?
   ```
2. **Verificar existência do quiz**
   - Tentar ler `data/personality-quiz.md`.
   - Se o arquivo não existir → iniciar o quiz (passo 3).
   - Se existir, procurar a linha `Concluído: true`.
     - Se encontrada → gerar `data/user-profile.md` a partir das respostas (passo 2‑b) e ir ao passo 5.
     - Se não encontrada → perguntar ao usuário:
       ```text
       Você já começou o quiz anteriormente. Deseja continuar de onde parou (c) ou reiniciar (r)?
       ```
       - **c** → continuar a partir da última pergunta não respondida.
       - **r** → sobrescrever `data/personality-quiz.md` e iniciar o quiz.
3. **Aplicar o Quiz** (perguntas feitas uma a uma, na ordem abaixo). Cada resposta deve ser gravada em `data/personality-quiz.md` no formato `chave: valor`.
   1. **Área de interesse**
      ```text
      Qual área mais te anima? Aqui estão suas opções: Frontend, Backend, Ciência de Dados, Mobile, DevOps, Full Stack, Governança de Dados, Design UX, Design UI, Liderança, RH, Marketing de Mídias Sociais, Growth Marketing, Gestão de Produtos ou Cibersegurança
      ```
   2. **Nível de experiência**
      ```text
      Como você descreveria seu nível de experiência atual? Escolha um: Júnior, Pleno ou Sênior
      ```
   3. **Tipo de oportunidade**
      ```text
      Como você prefere trabalhar? Opções: Remoto, Híbrido ou Presencial
      ```
   4. **Localização**
      ```text
      Onde você está localizado? Me diga sua cidade e estado, ou apenas diga 'Remoto'
      ```
   5. **Soft skills**
      ```text
      Quais são suas soft skills mais fortes? Pense em coisas como comunicação, trabalho em equipe, liderança, resolução de problemas — o que vier naturalmente para você
      ```
   6. **Objetivo de carreira**
      ```text
      Onde você se vê em sua carreira? Opções: Crescimento técnico, Transição de carreira, Primeiro emprego ou Trilha de liderança
      ```
   7. **Habilidades técnicas**
      ```text
      Quais habilidades técnicas você já tem? Apenas liste separadas por vírgulas — por exemplo: Python, SQL, Excel, Figma, Git
      ```
   - Ao final, acrescentar a linha `Concluído: true` ao arquivo.
4. **Gerar `data/user-profile.md`**
   - Ler todas as respostas de `data/personality-quiz.md`.
   - Transformar em um resumo estruturado, por exemplo:
     ```markdown
     # User Profile

     ## Respostas
     - area_de_interesse: <valor da pergunta 1>
     - nivel_experiencia: <valor da pergunta 2>
     - tipo_oportunidade: <valor da pergunta 3>
     - localizacao: <valor da pergunta 4>
     - soft_skills: <valor da pergunta 5>
     - objetivo_carreira: <valor da pergunta 6>
     - habilidades_tecnicas: <valor da pergunta 7>
     ```
   - Salvar em `data/user-profile.md`.
5. **Apresentar o Menu**
   ```text
   Escolha uma opção:
   A — Buscar vagas (Indeed, Catho, LinkedIn, Glassdoor, Infojobs)
   B — Encontrar cursos para preencher lacunas de habilidades (Alura)
   C — Praticar com uma entrevista simulada
   D — Refazer o quiz (sobrescreve o quiz e gera novo perfil)
   ```
6. **Processar a escolha**
   - **A** → usar a skill `dispatch.md` para despachar o agente **Scout**.
   - **B** → usar a skill `dispatch.md` para despachar o agente **Curator**.
   - **C** → despachar o agente **Coach** (não implementado ainda, mas o envelope deve ser enviado 6 vezes conforme especificado).
   - **D** → sobrescrever `data/personality-quiz.md` (remover conteúdo) e reiniciar o fluxo a partir do passo 3.
7. **Exibir a resposta do agente**
   - Quando o agente retornado enviar seu envelope de resposta, o Maestro deve mostrá‑lo ao usuário de forma legível.
8. **Loop**
   - Após exibir a resposta, voltar ao passo 5 (menu) para permitir novas interações.

---

### Integração
- O **Maestro** deve usar a skill `dispatch.md` para construir o envelope de despacho (exemplo já presente na skill).
- Para gerar o `user-profile.md` pode‑se usar a ferramenta `write_file`.
- As leituras de arquivos utilizam `read_file`.
- As interações de pergunta/resposta são realizadas pelo próprio agente (Zed) – aqui apenas descrevemos o fluxo lógico.

Este documento pode ser consumido por um script ou por um agente que interprete markdown como roteiro.
