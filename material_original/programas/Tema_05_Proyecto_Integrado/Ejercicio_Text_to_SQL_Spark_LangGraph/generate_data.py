"""
Generate random soccer match data for testing the Spark SQL agent.
"""
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_players(num_players=22):
    """Generate player data for a Spanish football match."""
    # Spanish first names
    first_names = [
        'Carlos', 'Miguel', 'Javier', 'Antonio', 'Luis', 'Francisco', 'Sergio',
        'Pablo', 'David', 'José', 'Raúl', 'Fernando', 'Alberto', 'Manuel',
        'Alejandro', 'Diego', 'Jorge', 'Andrés', 'Pedro', 'Rafael', 'Iván', 'Marcos'
    ]

    # Spanish last names
    last_names = [
        'García', 'Rodríguez', 'Martínez', 'López', 'González', 'Hernández',
        'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Flores', 'Rivera', 'Gómez',
        'Díaz', 'Reyes', 'Cruz', 'Morales', 'Jiménez', 'Ruiz', 'Álvarez', 'Romero', 'Castro'
    ]

    teams = ['Real Madrid'] * 11 + ['FC Barcelona'] * 11
    # Spanish positions: Portero (GK), Defensa (DF), Centrocampista (MF), Delantero (FW)
    positions = ['Portero', 'Defensa', 'Defensa', 'Defensa', 'Defensa',
                 'Centrocampista', 'Centrocampista', 'Centrocampista',
                 'Delantero', 'Delantero', 'Delantero']

    players = []
    used_names = set()

    for i in range(num_players):
        # Generate unique player name
        while True:
            first = random.choice(first_names)
            last = random.choice(last_names)
            full_name = f'{first} {last}'
            if full_name not in used_names:
                used_names.add(full_name)
                break

        players.append({
            'player_id': i + 1,
            'player_name': full_name,
            'team': teams[i],
            'position': positions[i % 11],
            'dorsal': (i % 11) + 1  # Jersey number 1-11
        })

    return pd.DataFrame(players)

def generate_match_events(num_events=2000):
    """Generate random football match events with Spanish terminology."""
    events = []

    # Spanish event types with realistic weights for a full 90-minute match
    event_types = [
        'pase', 'disparo', 'gol', 'entrada', 'intercepción', 'regate',
        'falta', 'córner', 'saque_de_banda', 'despeje', 'centro', 'parada',
        'fuera_de_juego', 'tarjeta_amarilla', 'tarjeta_roja', 'tiro_libre',
        'penalti', 'saque_de_meta', 'cabezazo', 'remate', 'asistencia'
    ]
    event_weights = [
        0.40,  # pase
        0.10,  # disparo
        0.015, # gol
        0.08,  # entrada
        0.07,  # intercepción
        0.05,  # regate
        0.04,  # falta
        0.025, # córner
        0.05,  # saque_de_banda
        0.03,  # despeje
        0.02,  # centro
        0.015, # parada
        0.02,  # fuera_de_juego
        0.01,  # tarjeta_amarilla
        0.002, # tarjeta_roja
        0.015, # tiro_libre
        0.003, # penalti
        0.04,  # saque_de_meta
        0.025, # cabezazo
        0.08,  # remate
        0.015  # asistencia
    ]

    start_time = datetime(2024, 4, 20, 15, 0, 0)
    current_time = start_time
    goals_team1 = 0
    goals_team2 = 0
    yellow_cards = {}  # Track yellow cards per player
    red_cards = set()  # Track red cards

    for i in range(num_events):
        event_type = random.choices(event_types, weights=event_weights)[0]

        # Exclude players with red cards
        available_players = [p for p in range(1, 23) if p not in red_cards]
        if not available_players:
            break

        # Assign player based on event type
        if event_type in ['gol', 'disparo', 'regate', 'centro', 'remate', 'cabezazo']:
            # Favor attackers and midfielders (positions 6-11 and 17-22)
            player_id = random.choice([p for p in available_players if p not in [1, 12]])
        elif event_type in ['parada', 'saque_de_meta']:
            # Only goalkeepers
            goalkeepers = [p for p in [1, 12] if p in available_players]
            if goalkeepers:
                player_id = random.choice(goalkeepers)
            else:
                continue
        elif event_type in ['despeje']:
            # Favor defenders (positions 2-5 and 13-16)
            defenders = [p for p in available_players if p in list(range(2, 6)) + list(range(13, 17))]
            player_id = random.choice(defenders) if defenders else random.choice(available_players)
        else:
            player_id = random.choice(available_players)

        # Determine team
        team = 'Real Madrid' if player_id <= 11 else 'FC Barcelona'

        # Soccer field coordinates: 105m x 68m
        x = random.uniform(0, 105)
        y = random.uniform(0, 68)

        # Adjust coordinates based on event type
        if event_type == 'gol':
            # Goals happen in the penalty area
            x = random.uniform(0, 16.5) if random.random() > 0.5 else random.uniform(88.5, 105)
            y = random.uniform(13.84, 54.16)  # Penalty area width
        elif event_type == 'córner':
            x = 0 if random.random() > 0.5 else 105
            y = 0 if random.random() > 0.5 else 68
        elif event_type in ['penalti', 'parada']:
            x = 11 if random.random() > 0.5 else 94  # Penalty spot
            y = 34
        elif event_type == 'fuera_de_juego':
            # Offsides happen in the attacking third
            x = random.uniform(70, 105) if player_id <= 11 else random.uniform(0, 35)
            y = random.uniform(0, 68)

        # Success rate depends on event type
        success_rates = {
            'pase': 0.78,
            'disparo': 0.30,
            'gol': 1.0,
            'entrada': 0.65,
            'intercepción': 0.70,
            'regate': 0.58,
            'falta': 0.0,
            'córner': 0.35,
            'saque_de_banda': 0.90,
            'despeje': 0.85,
            'centro': 0.45,
            'parada': 0.80,
            'fuera_de_juego': 0.0,
            'tarjeta_amarilla': 0.0,
            'tarjeta_roja': 0.0,
            'tiro_libre': 0.20,
            'penalti': 0.75,
            'saque_de_meta': 0.88,
            'cabezazo': 0.40,
            'remate': 0.35,
            'asistencia': 1.0
        }

        success = random.random() < success_rates.get(event_type, 0.5)

        # Time increment (events every 2-3 seconds on average for 2000 events in 90 mins)
        current_time += timedelta(seconds=random.uniform(2, 4))
        minute = int((current_time - start_time).total_seconds() / 60)

        # Stop at 90 minutes
        if minute >= 90:
            break

        # Track goals
        if event_type == 'gol':
            if player_id <= 11:
                goals_team1 += 1
            else:
                goals_team2 += 1

        # Track cards
        if event_type == 'tarjeta_amarilla':
            yellow_cards[player_id] = yellow_cards.get(player_id, 0) + 1
            # Second yellow = red card
            if yellow_cards[player_id] >= 2:
                red_cards.add(player_id)
        elif event_type == 'tarjeta_roja':
            red_cards.add(player_id)

        # Determine pressure
        pressure = random.random() < 0.30

        # Determine zone (defensive, middle, attacking third)
        if x < 35:
            zone = 'defensivo'
        elif x < 70:
            zone = 'medio'
        else:
            zone = 'ofensivo'

        events.append({
            'event_id': i + 1,
            'player_id': player_id,
            'team': team,
            'event_type': event_type,
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'x': round(x, 2),
            'y': round(y, 2),
            'success': success,
            'minute': minute,
            'presion': pressure,
            'zone': zone
        })

    return pd.DataFrame(events)

def main():
    """Generate and save data."""
    import os

    # Determine the correct path based on current directory
    prefix = 'data/'
    os.makedirs(prefix, exist_ok=True)

    print("Generando datos de jugadores...")
    players_df = generate_players()
    players_df.to_csv(f'{prefix}players.csv', index=False)
    print(f"Generados {len(players_df)} jugadores")
    print(f"  - {players_df[players_df['team'] == 'Real Madrid'].shape[0]} del Real Madrid")
    print(f"  - {players_df[players_df['team'] == 'FC Barcelona'].shape[0]} del FC Barcelona")

    print("\nGenerando eventos del partido...")
    events_df = generate_match_events()
    events_df.to_csv(f'{prefix}events.csv', index=False)
    print(f"Generados {len(events_df)} eventos")

    rm_goals = len(events_df[(events_df['event_type'] == 'gol') & (events_df['team'] == 'Real Madrid')])
    fcb_goals = len(events_df[(events_df['event_type'] == 'gol') & (events_df['team'] == 'FC Barcelona')])

    rm_events = events_df[events_df['team'] == 'Real Madrid']
    fcb_events = events_df[events_df['team'] == 'FC Barcelona']

    print(f"""
RESULTADO FINAL
Real Madrid {rm_goals} - {fcb_goals} FC Barcelona

Estadísticas del partido:
  - Duración: {events_df['minute'].max()} minutos
  - Total eventos: {len(events_df)}

  Real Madrid:
    - Pases: {len(rm_events[rm_events['event_type'] == 'pase'])}
    - Disparos: {len(rm_events[rm_events['event_type'] == 'disparo'])}
    - Faltas: {len(rm_events[rm_events['event_type'] == 'falta'])}

  FC Barcelona:
    - Pases: {len(fcb_events[fcb_events['event_type'] == 'pase'])}
    - Disparos: {len(fcb_events[fcb_events['event_type'] == 'disparo'])}
    - Faltas: {len(fcb_events[fcb_events['event_type'] == 'falta'])}

  Tarjetas:
    - Amarillas: {len(events_df[events_df['event_type'] == 'tarjeta_amarilla'])}
    - Rojas: {len(events_df[events_df['event_type'] == 'tarjeta_roja'])}
    - Fueras de juego: {len(events_df[events_df['event_type'] == 'fuera_de_juego'])}""")

    print(f"\nDatos guardados en {prefix}players.csv y {prefix}events.csv")

if __name__ == '__main__':
    main()
