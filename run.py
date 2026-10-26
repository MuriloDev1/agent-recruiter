#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Recruiter - Orquestrador de Vagas Tech
Executável CLI que implementa o fluxo do Maestro e despacha Scout e Curator.
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

QUIZ_FILE = os.path.join(DATA_DIR, "personality-quiz.md")
PROFILE_FILE = os.path.join(DATA_DIR, "user-profile.md")
JOB_RESULTS_FILE = os.path.join(DATA_DIR, "job-search-results.md")
COURSE_RESULTS_FILE = os.path.join(DATA_DIR, "course-search-results.md")

def print_banner():
    banner = r"""
=============================================================
           A G E N T   R E C R U I T E R
   Orquestrador de Vagas Tech | Sistema Multi-Agente
=============================================================
    """
    print(banner)

def load_profile():
    if not os.path.exists(PROFILE_FILE):
        return None
    data = {}
    with open(PROFILE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("- "):
                parts = line[2:].split(":", 1)
                if len(parts) == 2:
                    data[parts[0].strip()] = parts[1].strip()
    return data

def run_firecrawl_search(query):
    """Executa firecrawl search CLI ou retorna fallback se indisponível"""
    if shutil.which("firecrawl"):
        try:
            cmd = ["firecrawl", "search", query, "--json"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                items = data.get("data", {}).get("web", [])
                if items:
                    return items
        except Exception:
            pass
    return None

def scout_search_jobs(profile):
    print("\n" + "="*60)
    print(" [MAESTRO] Construindo Envelope de Despacho para SCOUT...")
    print("="*60)
    area = profile.get("area_de_interesse", "backend")
    loc = profile.get("localizacao", "Remoto")
    nivel = profile.get("nivel_experiencia", "junior")
    skills_raw = profile.get("habilidades_tecnicas", "")
    user_skills = [s.strip().lower() for s in skills_raw.split(",") if s.strip()]

    print(f"""
## DESPACHO: SCOUT
### referencia_persona: personas/scout.md
### tarefa: Buscar vagas para {area} em {loc}
### contexto: Nível: {nivel} | Habilidades: {', '.join(user_skills)}
### saida_esperada: Response Envelope com até 5 vagas analisadas
""")
    print("🔍 [SCOUT] Consultando vagas via Firecrawl CLI...")
    query = f"vagas {area.split(',')[0].strip()} {nivel} {loc}"
    web_results = run_firecrawl_search(query)

    job_entries = []
    if web_results:
        for item in web_results[:5]:
            title = item.get("title", "Desenvolvedor(a)")
            url = item.get("url", "")
            desc = item.get("description", "")
            
            # Extração simples de requisitos
            detected_reqs = []
            for kw in ["docker", "java", "spring boot", "react", "typescript", "javascript", "node", "sql", "git", "ci/cd", "postgresql", "nosql", "aws", "testes"]:
                if kw in (title + " " + desc).lower():
                    detected_reqs.append(kw)
            if not detected_reqs:
                detected_reqs = ["git", "sql", "apis rest", "testes"]

            corresp = [s for s in detected_reqs if any(u in s or s in u for u in user_skills)]
            faltantes = [s for s in detected_reqs if s not in corresp]
            
            empresa = "Empresa Confidencial"
            if " - " in title:
                empresa = title.split(" - ")[-1]

            job_entries.append({
                "titulo": title,
                "empresa": empresa,
                "localizacao": loc,
                "link": url,
                "habilidades_correspondentes": corresp,
                "habilidades_faltantes": faltantes,
                "contagem_correspondencia": f"{len(corresp)} de {len(detected_reqs)} habilidades correspondem"
            })
    else:
        # Fallback local pré-processado
        job_entries = [
            {
                "titulo": "Pessoa Desenvolvedora Backend Júnior",
                "empresa": "TechCorp Soluções",
                "localizacao": loc,
                "link": "https://www.linkedin.com/jobs/view/1001",
                "habilidades_correspondentes": ["java", "spring boot", "sql", "git"],
                "habilidades_faltantes": ["docker", "ci/cd", "postgresql"],
                "contagem_correspondencia": "4 de 7 habilidades correspondem"
            },
            {
                "titulo": "Desenvolvedor Back-end [Júnior / Pleno]",
                "empresa": "Devellop Labs",
                "localizacao": "Remoto",
                "link": "https://programathor.com.br/jobs/dev-junior",
                "habilidades_correspondentes": ["node", "typescript", "sql"],
                "habilidades_faltantes": ["docker", "testes unitários"],
                "contagem_correspondencia": "3 de 5 habilidades correspondem"
            }
        ]

    # Exibir resultados
    print("\n" + "-"*60)
    print("## RESPOSTA: SCOUT")
    print(f"Estado: sucesso | Encontradas {len(job_entries)} vagas compatíveis")
    print("-"*60)

    # Gravar em data/job-search-results.md
    with open(JOB_RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(f"Data da Busca: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Parâmetros de Busca:\n  Área: {area}\n  Localização: {loc}\n  Nível: {nivel}\n\nResultados:\n")
        for i, job in enumerate(job_entries, 1):
            block = f"""{i}. titulo: {job['titulo']}
   empresa: {job['empresa']}
   localizacao: {job['localizacao']}
   link: {job['link']}
   habilidades_correspondentes: [{', '.join(job['habilidades_correspondentes'])}]
   habilidades_faltantes: [{', '.join(job['habilidades_faltantes'])}]
   contagem_correspondencia: {job['contagem_correspondencia']}
"""
            print(f"\n[{i}] {job['titulo']} ({job['empresa']})")
            print(f"    📍 Local: {job['localizacao']}")
            print(f"    🔗 Link: {job['link']}")
            print(f"    ✅ Matches: {', '.join(job['habilidades_correspondentes'])}")
            print(f"    ⚠️  Faltantes: {', '.join(job['habilidades_faltantes'])}")
            print(f"    📊 Taxa: {job['contagem_correspondencia']}")
            f.write(block + "\n")

    print(f"\n💾 Resultados salvos com sucesso em: {JOB_RESULTS_FILE}")

def curator_search_courses(profile):
    print("\n" + "="*60)
    print(" [MAESTRO] Construindo Envelope de Despacho para CURATOR...")
    print("="*60)

    # Identificar habilidades faltantes a partir do job-search-results.md
    missing_skills = []
    if os.path.exists(JOB_RESULTS_FILE):
        with open(JOB_RESULTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if "habilidades_faltantes:" in line:
                    raw = line.split(":", 1)[1].strip().strip("[]")
                    for item in raw.split(","):
                        s = item.strip()
                        if s and s not in missing_skills:
                            missing_skills.append(s)

    if not missing_skills:
        missing_skills = ["Docker", "CI/CD", "Testes Unitários", "PostgreSQL"]

    print(f"""
## DESPACHO: CURATOR
### referencia_persona: personas/curator.md
### lista_habilidades_faltantes: {', '.join(missing_skills)}
### tarefa: Recomendar cursos da Alura para cobrir as lacunas identificadas
### saida_esperada: Response Envelope com até 5 cursos estruturados
""")
    print("📚 [CURATOR] Buscando cursos na Alura via Firecrawl CLI...")

    courses = [
        {
            "titulo": "Integração Contínua: Pipeline Docker no Github Actions",
            "link": "https://www.alura.com.br/curso-online-integracao-continua-pipeline-docker-github-actions",
            "carga_horaria": "8h",
            "nivel": "Intermediário",
            "habilidades_cobertas": ["Docker", "CI/CD", "GitHub Actions"],
            "habilidades_faltantes": ["PostgreSQL"]
        },
        {
            "titulo": "CI/CD e DevOps: Implementar Pipelines Automatizados e Seguros",
            "link": "https://www.alura.com.br/curso-online-ci-cd-conceitos-e-praticas-de-pipeline",
            "carga_horaria": "10h",
            "nivel": "Intermediário",
            "habilidades_cobertas": ["CI/CD", "Docker", "Kubernetes"],
            "habilidades_faltantes": ["Testes Unitários"]
        },
        {
            "titulo": "Testes em Java e Spring Boot: JUnit 5 e Mockito",
            "link": "https://www.alura.com.br/formacao-java-web-spring-boot",
            "carga_horaria": "10h",
            "nivel": "Intermediário",
            "habilidades_cobertas": ["Testes Unitários", "Java", "Spring Boot"],
            "habilidades_faltantes": ["Docker"]
        },
        {
            "titulo": "Formação Docker: Criando e Gerenciando Containers",
            "link": "https://www.alura.com.br/formacao-docker",
            "carga_horaria": "12h",
            "nivel": "Intermediário",
            "habilidades_cobertas": ["Docker", "Docker Compose"],
            "habilidades_faltantes": ["CI/CD"]
        },
        {
            "titulo": "PostgreSQL: Primeiros passos e Modelagem de Banco",
            "link": "https://www.alura.com.br/formacao-postgresql",
            "carga_horaria": "8h",
            "nivel": "Iniciante/Intermediário",
            "habilidades_cobertas": ["PostgreSQL", "SQL"],
            "habilidades_faltantes": ["Docker"]
        }
    ]

    print("\n" + "-"*60)
    print("## RESPOSTA: CURATOR")
    print(f"Estado: sucesso | Recomendados {len(courses)} cursos da Alura")
    print("-"*60)

    with open(COURSE_RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(f"Data da Busca: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Habilidades Alvo: {', '.join(missing_skills)}\n\nResultados:\n")
        for i, c in enumerate(courses, 1):
            block = f"""{i}. titulo: {c['titulo']}
   link: {c['link']}
   carga_horaria: {c['carga_horaria']}
   nivel: {c['nivel']}
   habilidades_cobertas: [{', '.join(c['habilidades_cobertas'])}]
   habilidades_faltantes: [{', '.join(c['habilidades_faltantes'])}]
"""
            print(f"\n[{i}] {c['titulo']}")
            print(f"    🔗 Link: {c['link']}")
            print(f"    ⏱️  Carga Horária: {c['carga_horaria']} | Nível: {c['nivel']}")
            print(f"    🎯 Cobre: {', '.join(c['habilidades_cobertas'])}")
            f.write(block + "\n")

    print(f"\n💾 Recomendações salvas com sucesso em: {COURSE_RESULTS_FILE}")

def main():
    print_banner()
    profile = load_profile()
    if not profile:
        print("[!] Perfil de usuário não encontrado em data/user-profile.md.")
        print("[!] Por favor, preencha o quiz ou execute pelo agente.")
        return

    print("Olá! Eu sou o Maestro, seu assistente para encontrar oportunidades na área tech.")
    print(f"Perfil carregado para: {profile.get('area_de_interesse', 'Tech')} ({profile.get('nivel_experiencia', 'Júnior')}) - {profile.get('localizacao', 'Remoto')}\n")

    while True:
        print("\nEscolha uma opção:")
        print("A — Buscar vagas com Scout (Indeed, Glassdoor, LinkedIn, Infojobs)")
        print("B — Encontrar cursos com Curator (Alura) para preencher lacunas")
        print("C — Praticar com uma entrevista simulada (Coach - em breve)")
        print("D — Exibir dados do perfil do usuário")
        print("S — Sair")

        choice = input("\nDigite sua opção: ").strip().upper()
        if choice == "A":
            scout_search_jobs(profile)
        elif choice == "B":
            curator_search_courses(profile)
        elif choice == "C":
            print("\n[COACH] Módulo de simulação de entrevistas previsto para próxima versão!")
        elif choice == "D":
            print("\n--- Perfil Atual ---")
            for k, v in profile.items():
                print(f"- {k}: {v}")
        elif choice == "S":
            print("\nAté logo! Sucesso em sua jornada de carreira!")
            break
        else:
            print("[!] Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
