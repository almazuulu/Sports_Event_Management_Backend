# Game API Documentation

This document provides comprehensive information about the Game API endpoints for the Sports Event Management system, including descriptions, example requests, and responses.

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Game Endpoints](#game-endpoints)
   - [List Games](#list-games)
   - [Create Game](#create-game)
   - [Retrieve Game](#retrieve-game)
   - [Update Game](#update-game)
   - [Partial Update Game](#partial-update-game)
   - [Delete Game](#delete-game)
   - [Update Game Status](#update-game-status)
   - [Upcoming Games](#upcoming-games)
4. [Game Team Endpoints](#game-team-endpoints)
   - [List Game Teams](#list-game-teams)
   - [Create Game Team](#create-game-team)
   - [Retrieve Game Team](#retrieve-game-team)
   - [Update Game Team](#update-game-team)
   - [Delete Game Team](#delete-game-team)
5. [Game Player Endpoints](#game-player-endpoints)
   - [List Game Players](#list-game-players)
   - [Create Game Player](#create-game-player)
   - [Bulk Create Game Players](#bulk-create-game-players)
   - [Retrieve Game Player](#retrieve-game-player)
   - [Update Game Player](#update-game-player)
   - [Delete Game Player](#delete-game-player)

## Introduction

The Game API provides endpoints for managing sports games, team assignments, and player selections for games. This API is part of the Multi-Sport Event Management System, which supports organizing sports tournaments, managing teams, scheduling games, and tracking scores.

## Authentication

Most endpoints require authentication using JWT (JSON Web Token). Include the token in the Authorization header:

```
Authorization: Bearer {your_token}
```

Different endpoints have different permission requirements:
- **Admin Users**: Can perform all operations
- **Scorekeepers**: Can update game status for games they are assigned to
- **Team Managers/Captains**: Can manage player selections for their teams
- **Public Users**: Can view public game information

## Game Endpoints

### List Games

Retrieves a paginated list of all games with basic information.

**Endpoint**: `GET /api/games/games/`

**Parameters**:
- `sport_event` (optional): Filter by sport event ID
- `status` (optional): Filter by game status (`scheduled`, `ongoing`, `completed`, `cancelled`)
- `game_teams__team` (optional): Filter by team ID
- `search` (optional): Search in name, description, and location
- `ordering` (optional): Order by field (e.g., `start_datetime`, `-start_datetime`)

**Permissions**: Public access

**Response Example**:
```json
{
  "count": 25,
  "next": "http://example.com/api/games/games/?page=2",
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "name": "Semifinals - Round 1",
      "sport_event_name": "Annual Basketball Tournament 2025",
      "start_datetime": "2025-04-15T14:00:00Z",
      "time_display": "14:00",
      "location": "Main Court",
      "status": "scheduled",
      "teams": [
        {
          "team_name": "Thunderbolts",
          "designation": "Team A"
        },
        {
          "team_name": "Lightning Strikes",
          "designation": "Team B"
        }
      ]
    }
  ]
}
```

### Create Game

Creates a new game with associated information.

**Endpoint**: `POST /api/games/games/`

**Permissions**: Admin only

**Request Example**:
```json
{
  "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
  "name": "Semifinals - Round 1",
  "description": "First semifinal match",
  "location": "Main Court",
  "start_datetime": "2025-04-15T14:00:00Z",
  "end_datetime": "2025-04-15T16:00:00Z",
  "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afa8"
}
```

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
  "sport_event_name": "Annual Basketball Tournament 2025",
  "name": "Semifinals - Round 1",
  "description": "First semifinal match",
  "location": "Main Court",
  "start_datetime": "2025-04-15T14:00:00Z",
  "end_datetime": "2025-04-15T16:00:00Z",
  "time_display": "14:00",
  "status": "scheduled",
  "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
  "scorekeeper_name": "John Scorer",
  "teams": [],
  "created_at": "2025-04-01T10:30:00Z"
}
```

### Retrieve Game

Retrieves detailed information about a specific game, including teams and players.

**Endpoint**: `GET /api/games/games/{id}/`

**Parameters**:
- `id` (path parameter): Game ID (UUID)

**Permissions**: Public access

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
  "sport_event_name": "Annual Basketball Tournament 2025",
  "name": "Semifinals - Round 1",
  "description": "First semifinal match",
  "location": "Main Court",
  "start_datetime": "2025-04-15T14:00:00Z",
  "end_datetime": "2025-04-15T16:00:00Z",
  "time_display": "14:00",
  "status": "scheduled",
  "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
  "scorekeeper_name": "John Scorer",
  "teams": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afaa",
      "team_name": "Thunderbolts",
      "designation": "Team A",
      "players": [
        {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afab",
          "player": "3fa85f64-5717-4562-b3fc-2c963f66afac",
          "name": "John Smith",
          "jersey_number": 23,
          "position": "Forward",
          "is_captain_for_game": true,
          "notes": "Starting player"
        }
      ]
    },
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afad",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afae",
      "team_name": "Lightning Strikes",
      "designation": "Team B",
      "players": [
        {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afaf",
          "player": "3fa85f64-5717-4562-b3fc-2c963f66afb0",
          "name": "Michael Johnson",
          "jersey_number": 12,
          "position": "Guard",
          "is_captain_for_game": true,
          "notes": ""
        }
      ]
    }
  ],
  "created_at": "2025-04-01T10:30:00Z",
  "updated_at": "2025-04-01T10:30:00Z"
}
```

### Update Game

Completely updates all fields of an existing game.

**Endpoint**: `PUT /api/games/games/{id}/`

**Parameters**:
- `id` (path parameter): Game ID (UUID)

**Permissions**: Admin only

**Request Example**:
```json
{
  "name": "Finals - Championship Game",
  "description": "Championship final match",
  "location": "Olympic Stadium",
  "start_datetime": "2025-04-20T15:00:00Z",
  "end_datetime": "2025-04-20T17:00:00Z",
  "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afa8"
}
```

**Response Example**: Same as Retrieve Game

### Partial Update Game

Updates specific fields of an existing game.

**Endpoint**: `PATCH /api/games/games/{id}/`

**Parameters**:
- `id` (path parameter): Game ID (UUID)

**Permissions**: Admin only

**Request Example**:
```json
{
  "location": "Olympic Stadium Main Court",
  "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afb1"
}
```

**Response Example**: Same as Retrieve Game

### Delete Game

Permanently deletes a game from the system.

**Endpoint**: `DELETE /api/games/games/{id}/`

**Parameters**:
- `id` (path parameter): Game ID (UUID)

**Permissions**: Admin only

**Response**: HTTP 204 No Content

### Update Game Status

Updates the status of a game (e.g., from scheduled to ongoing, or from ongoing to completed).

**Endpoint**: `PATCH /api/games/games/{id}/update-status/`

**Parameters**:
- `id` (path parameter): Game ID (UUID)

**Permissions**: Admin or assigned scorekeeper

**Request Example**:
```json
{
  "status": "ongoing"
}
```

**Response Example**: Same as Retrieve Game

### Upcoming Games

Gets a list of upcoming games for dashboard or homepage use. Only shows scheduled and ongoing games.

**Endpoint**: `GET /api/games/games/upcoming/`

**Parameters**:
- `sport_event` (optional): Filter by sport event ID
- `team` (optional): Filter by team ID

**Permissions**: Public access

**Response Example**:
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "name": "Semifinals - Round 1",
    "sport_event_name": "Annual Basketball Tournament 2025",
    "start_datetime": "2025-04-15T14:00:00Z",
    "location": "Main Court",
    "teams": [
      "Thunderbolts vs Lightning Strikes"
    ]
  }
]
```

## Game Team Endpoints

These endpoints manage the association between games and teams, defining which teams participate in each game.

### List Game Teams

Returns a list of all game team associations with filtering options.

**Endpoint**: `GET /api/games/game-teams/`

**Parameters**:
- `game` (optional): Filter by game ID
- `team` (optional): Filter by team ID 
- `designation` (optional): Filter by team designation (e.g., `team_a`, `team_b`, `home`, `away`)

**Permissions**: Public access

**Response Example**:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "game": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "game_name": "Semifinals - Round 1",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afaa",
      "team_name": "Thunderbolts",
      "designation": "team_a",
      "designation_display": "Team A",
      "selected_players_count": 10
    }
  ]
}
```

### Create Game Team

Creates a new game team association, assigning a team to a game with a specific designation.

**Endpoint**: `POST /api/games/game-teams/`

**Permissions**: Admin only

**Request Example**:
```json
{
  "game": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "team": "3fa85f64-5717-4562-b3fc-2c963f66afaa",
  "designation": "team_a"
}
```

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
  "game": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "game_name": "Semifinals - Round 1",
  "team": "3fa85f64-5717-4562-b3fc-2c963f66afaa",
  "team_name": "Thunderbolts",
  "designation": "team_a",
  "designation_display": "Team A",
  "selected_players_count": 0
}
```

### Retrieve Game Team

Gets detailed information about a specific game team association, including selected players.

**Endpoint**: `GET /api/games/game-teams/{id}/`

**Parameters**:
- `id` (path parameter): Game Team ID (UUID)

**Permissions**: Public access

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
  "game": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "game_name": "Semifinals - Round 1",
  "team": "3fa85f64-5717-4562-b3fc-2c963f66afaa",
  "team_name": "Thunderbolts",
  "designation": "team_a",
  "designation_display": "Team A",
  "selected_players": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afad",
      "player": "3fa85f64-5717-4562-b3fc-2c963f66afae",
      "player_name": "John Smith",
      "jersey_number": 23,
      "is_captain_for_game": true,
      "position": "Forward",
      "notes": "Starting player"
    }
  ]
}
```

### Update Game Team

Updates the details of a game team association, typically the designation.

**Endpoint**: `PUT /api/games/game-teams/{id}/`

**Parameters**:
- `id` (path parameter): Game Team ID (UUID)

**Permissions**: Admin only

**Request Example**:
```json
{
  "designation": "home"
}
```

**Response Example**: Same as List Game Teams

### Delete Game Team

Removes a team from a game.

**Endpoint**: `DELETE /api/games/game-teams/{id}/`

**Parameters**:
- `id` (path parameter): Game Team ID (UUID)

**Permissions**: Admin only

**Response**: HTTP 204 No Content

## Game Player Endpoints

These endpoints manage the selection of players for games, defining which players will participate in each game.

### List Game Players

Returns a list of all game player selections with filtering options.

**Endpoint**: `GET /api/games/game-players/`

**Parameters**:
- `game_team` (optional): Filter by game team ID
- `player` (optional): Filter by player ID
- `is_captain_for_game` (optional): Filter by captain status

**Permissions**: Public access

**Response Example**:
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afad",
      "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "game_name": "Semifinals - Round 1",
      "team_name": "Thunderbolts",
      "player": "3fa85f64-5717-4562-b3fc-2c963f66afae",
      "player_name": "John Smith",
      "jersey_number": 23,
      "is_captain_for_game": true,
      "position": "Forward",
      "notes": "Starting player"
    }
  ]
}
```

### Create Game Player

Adds a player to a game team.

**Endpoint**: `POST /api/games/game-players/`

**Permissions**: Admin or team manager/captain

**Request Example**:
```json
{
  "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
  "player": "3fa85f64-5717-4562-b3fc-2c963f66afae",
  "is_captain_for_game": true,
  "position": "Forward",
  "notes": "Starting player"
}
```

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afad",
  "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
  "game_name": "Semifinals - Round 1",
  "team_name": "Thunderbolts",
  "player": "3fa85f64-5717-4562-b3fc-2c963f66afae",
  "player_name": "John Smith",
  "jersey_number": 23,
  "is_captain_for_game": true,
  "position": "Forward",
  "notes": "Starting player"
}
```

### Bulk Create Game Players

Efficiently adds multiple players to a game team in a single API call.

**Endpoint**: `POST /api/games/game-players/bulk-create/`

**Permissions**: Admin or team manager/captain

**Request Example**:
```json
[
  {
    "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    "player": "3fa85f64-5717-4562-b3fc-2c963f66afae",
    "is_captain_for_game": true,
    "position": "Forward"
  },
  {
    "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    "player": "3fa85f64-5717-4562-b3fc-2c963f66afaf",
    "position": "Guard"
  }
]
```

**Response Example**:
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afad",
    "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    "game_name": "Semifinals - Round 1",
    "team_name": "Thunderbolts",
    "player": "3fa85f64-5717-4562-b3fc-2c963f66afae",
    "player_name": "John Smith",
    "jersey_number": 23,
    "is_captain_for_game": true,
    "position": "Forward",
    "notes": ""
  },
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afb1",
    "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    "game_name": "Semifinals - Round 1",
    "team_name": "Thunderbolts",
    "player": "3fa85f64-5717-4562-b3fc-2c963f66afaf",
    "player_name": "Michael Johnson",
    "jersey_number": 12,
    "is_captain_for_game": false,
    "position": "Guard",
    "notes": ""
  }
]
```

### Retrieve Game Player

Gets detailed information about a specific game player selection.

**Endpoint**: `GET /api/games/game-players/{id}/`

**Parameters**:
- `id` (path parameter): Game Player ID (UUID)

**Permissions**: Public access

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afad",
  "game_team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
  "game_name": "Semifinals - Round 1",
  "team_name": "Thunderbolts",
  "player": "3fa85f64-5717-4562-b3fc-2c963f66afae",
  "player_name": "John Smith",
  "jersey_number": 23,
  "is_captain_for_game": true,
  "position": "Forward",
  "notes": "Starting player"
}
```

### Update Game Player

Updates the details of a game player selection, such as position or captain status.

**Endpoint**: `PUT /api/games/game-players/{id}/`

**Parameters**:
- `id` (path parameter): Game Player ID (UUID)

**Permissions**: Admin or team manager/captain

**Request Example**:
```json
{
  "is_captain_for_game": false,
  "position": "Center",
  "notes": "Substitute player"
}
```

**Response Example**: Same as Retrieve Game Player with updated fields

### Delete Game Player

Removes a player from a game team.

**Endpoint**: `DELETE /api/games/game-players/{id}/`

**Parameters**:
- `id` (path parameter): Game Player ID (UUID)

**Permissions**: Admin or team manager/captain

**Response**: HTTP 204 No Content
