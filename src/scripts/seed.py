"""Script para popular banco com dados fictícios (Issue #27)."""
import sys
from pathlib import Path
from datetime import date, datetime, timedelta
from faker import Faker

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal
from app.core.security import get_password_hash
from app.models import User, UserRole, Team, Athlete, Training, Attendance, Evaluation


fake = Faker("pt_BR")


def seed_database():
    """Popula banco com dados fictícios para testes e demonstração."""
    db: Session = SessionLocal()

    try:
        print("🌱 Iniciando seed do banco de dados...")

        # 1. Cria usuários (treinadores)
        print("  👤 Criando treinadores...")
        coaches = []
        for i in range(3):
            coach = User(
                name=fake.name(),
                email=fake.unique.email(),
                hashed_password=get_password_hash("senha123"),
                role=UserRole.COACH,
            )
            db.add(coach)
            coaches.append(coach)
        db.commit()
        for c in coaches:
            db.refresh(c)
        print(f"     ✓ {len(coaches)} treinadores criados")

        # 2. Cria equipes para cada treinador
        print("  🏐 Criando equipes...")
        categories = ["sub-13", "sub-15", "sub-17", "sub-19", "adulto", "master"]
        teams = []
        for coach in coaches:
            for _ in range(fake.random_int(1, 2)):
                team = Team(
                    name=fake.unique.company() + " Vôlei",
                    category=fake.random_element(categories),
                    coach_id=coach.id,
                )
                db.add(team)
                teams.append(team)
        db.commit()
        for t in teams:
            db.refresh(t)
        print(f"     ✓ {len(teams)} equipes criadas")

        # 3. Cria atletas para cada equipe
        print("  🏃 Criando atletas...")
        positions = ["levantador", "ponteiro", "oposto", "central", "líbero", None]
        athletes = []
        for team in teams:
            num_athletes = fake.random_int(8, 14)
            for _ in range(num_athletes):
                # Idade compatível com categoria
                cat = team.category
                if "sub-13" in cat:
                    birth_year = fake.random_int(2013, 2015)
                elif "sub-15" in cat:
                    birth_year = fake.random_int(2011, 2013)
                elif "sub-17" in cat:
                    birth_year = fake.random_int(2009, 2011)
                elif "sub-19" in cat:
                    birth_year = fake.random_int(2007, 2009)
                elif "master" in cat:
                    birth_year = fake.random_int(1970, 1990)
                else:  # adulto
                    birth_year = fake.random_int(1990, 2005)

                athlete = Athlete(
                    team_id=team.id,
                    name=fake.name(),
                    birth_date=date(birth_year, fake.random_int(1, 12), fake.random_int(1, 28)),
                    position=fake.random_element(positions),
                )
                db.add(athlete)
                athletes.append(athlete)
        db.commit()
        for a in athletes:
            db.refresh(a)
        print(f"     ✓ {len(athletes)} atletas criados")

        # 4. Cria treinos para cada equipe (últimos 3 meses)
        print("  📅 Criando treinos...")
        trainings = []
        themes = [
            "Fundamentos de passe e recepção",
            "Saque: flutuante e jump",
            "Ataque: aproximação e corte",
            "Bloqueio: posicionamento e tempo",
            "Defesa: leitura e cobertura",
            "Sistema defensivo 5-1",
            "Sistema ofensivo 6-2",
            "Transição defesa-ataque",
            "Trabalho de saque e bloqueio",
            "Jogo treino situacional",
        ]
        for team in teams:
            num_trainings = fake.random_int(8, 16)
            base_date = date.today() - timedelta(days=90)
            for i in range(num_trainings):
                training_date = base_date + timedelta(days=fake.random_int(0, 90))
                training = Training(
                    team_id=team.id,
                    date=training_date,
                    theme=fake.random_element(themes),
                    notes=fake.paragraph(nb_sentences=2) if fake.boolean(30) else None,
                )
                db.add(training)
                trainings.append(training)
        db.commit()
        for t in trainings:
            db.refresh(t)
        print(f"     ✓ {len(trainings)} treinos criados")

        # 5. Cria presenças (chamadas)
        print("  ✅ Criando presenças...")
        attendances = []
        for training in trainings:
            # Busca atletas ativos da equipe no momento do treino
            team_athletes = [a for a in athletes if a.team_id == training.team_id and a.is_active]
            if not team_athletes:
                continue

            # 70-95% de presença
            present_count = int(len(team_athletes) * fake.random_int(70, 95) / 100)
            present_athletes = fake.random_elements(team_athletes, length=present_count, unique=True)
            present_ids = {a.id for a in present_athletes}

            for athlete in team_athletes:
                attendance = Attendance(
                    training_id=training.id,
                    athlete_id=athlete.id,
                    present=athlete.id in present_ids,
                )
                db.add(attendance)
                attendances.append(attendance)
        db.commit()
        print(f"     ✓ {len(attendances)} registros de presença criados")

        # 6. Cria avaliações (2-4 por atleta ao longo do tempo)
        print("  📊 Criando avaliações...")
        evaluations = []
        for athlete in athletes:
            num_evals = fake.random_int(2, 4)
            eval_dates = sorted([
                fake.date_between(start_date=date.today() - timedelta(days=120), end_date=date.today())
                for _ in range(num_evals)
            ])

            # Simula evolução: notas tendem a subir
            base_ratings = {
                "pass": fake.random_int(2, 3),
                "serve": fake.random_int(2, 3),
                "attack": fake.random_int(2, 3),
                "block": fake.random_int(1, 2),
                "defense": fake.random_int(2, 3),
            }

            for i, eval_date in enumerate(eval_dates):
                # Progressão leve
                progress = i * fake.random_int(0, 1)
                evaluation = Evaluation(
                    athlete_id=athlete.id,
                    evaluator_id=athlete.team.coach_id,
                    date=datetime.combine(eval_date, datetime.min.time()),
                    pass_rating=min(5, base_ratings["pass"] + progress + fake.random_int(-1, 1)),
                    serve_rating=min(5, base_ratings["serve"] + progress + fake.random_int(-1, 1)),
                    attack_rating=min(5, base_ratings["attack"] + progress + fake.random_int(-1, 1)),
                    block_rating=min(5, base_ratings["block"] + progress + fake.random_int(-1, 1)),
                    defense_rating=min(5, base_ratings["defense"] + progress + fake.random_int(-1, 1)),
                    notes=fake.paragraph(nb_sentences=2) if fake.boolean(40) else None,
                )
                # Garante notas entre 1-5
                for field in ["pass_rating", "serve_rating", "attack_rating", "block_rating", "defense_rating"]:
                    val = getattr(evaluation, field)
                    setattr(evaluation, field, max(1, min(5, val)))

                db.add(evaluation)
                evaluations.append(evaluation)
        db.commit()
        print(f"     ✓ {len(evaluations)} avaliações criadas")

        print("\n✅ Seed concluído com sucesso!")
        print(f"""
Resumo:
  👤 Treinadores: {len(coaches)}
  🏐 Equipes: {len(teams)}
  🏃 Atletas: {len(athletes)}
  📅 Treinos: {len(trainings)}
  ✅ Presenças: {len(attendances)}
  📊 Avaliações: {len(evaluations)}
        """)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro durante seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()