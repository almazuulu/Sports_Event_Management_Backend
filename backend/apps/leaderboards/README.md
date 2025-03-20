# Leaderboards API Documentation

This document provides comprehensive information about the Leaderboards API endpoints for the Sports Event Management system, including descriptions, example requests, and responses.

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Leaderboard Endpoints](#leaderboard-endpoints)
   - [List Leaderboards](#list-leaderboards)
   - [Retrieve Leaderboard](#retrieve-leaderboard)
   - [Create Leaderboard](#create-leaderboard)
   - [Update Leaderboard](#update-leaderboard)
   - [Delete Leaderboard](#delete-leaderboard)
   - [Calculate Leaderboard](#calculate-leaderboard)
   - [Finalize Leaderboard](#finalize-leaderboard)
   - [Team Leaderboards](#team-leaderboards)
4. [Leaderboard Entry Endpoints](#leaderboard-entry-endpoints)
   - [List Leaderboard Entries](#list-leaderboard-entries)
   - [Retrieve Leaderboard Entry](#retrieve-leaderboard-entry)

## Introduction

The Leaderboards API provides endpoints for tracking and displaying team standings in sport events. It supports automatic calculation of leaderboards based on game results and allows administration of tournament standings.

## Authentication

Most endpoints are publicly accessible for read operations. Administrative operations require authentication using JWT (JSON Web Token). Include the token in the Authorization header:

```
Authorization: Bearer {your_token}
```

Different endpoints have different permission requirements:
- **Admin Users**: Can perform all operations including creating, calculating, and finalizing leaderboards
- **Team Managers/Players/Scorekeepers**: Can view leaderboards and standings
- **Public Users**: Can view leaderboards and standings

## Leaderboard Endpoints

### List Leaderboards

Retrieves a paginated list of all leaderboards with summary information.

**Endpoint**: `GET /api/leaderboards/`

**Parameters**:
- `sport_event` (optional): Filter by sport event ID
- `is_final` (optional): Filter by final status (`true`/`false`)
- `search` (optional): Search in sport event name
- `ordering` (optional): Order by field (e.g., `last_updated`, `-last_updated`)

**Permissions**: Public access

**Response Example**:
```json
{
  "count": 3,
  "next": "http://example.com/api/leaderboards/?page=2",
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
      "sport_event_name": "Annual Football Tournament 2025",
      "sport_type": "Football",
      "last_updated": "2025-03-15T14:30:00Z",
      "is_final": false,
      "teams_count": 8
    }
  ]
}
```

### Retrieve Leaderboard

Gets detailed information about a specific leaderboard including all team entries.

**Endpoint**: `GET /api/leaderboards/{id}/`

**Parameters**:
- `id` (path parameter): Leaderboard ID (UUID)

**Permissions**: Public access

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
  "sport_event_name": "Annual Football Tournament 2025",
  "last_updated": "2025-03-15T14:30:00Z",
  "is_final": false,
  "entries": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "team_name": "Eagles",
      "position": 1,
      "played": 5,
      "won": 4,
      "drawn": 0,
      "lost": 1,
      "points": 12,
      "goals_for": 12,
      "goals_against": 5,
      "goal_difference": 7,
      "clean_sheets": 2,
      "yellow_cards": 3,
      "red_cards": 0
    },
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afb0",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afb1",
      "team_name": "Falcons",
      "position": 2,
      "played": 5,
      "won": 3,
      "drawn": 1,
      "lost": 1,
      "points": 10,
      "goals_for": 10,
      "goals_against": 6,
      "goal_difference": 4,
      "clean_sheets": 1,
      "yellow_cards": 5,
      "red_cards": 1
    }
  ]
}
```

### Create Leaderboard

Creates a new leaderboard for a sport event.

**Endpoint**: `POST /api/leaderboards/`

**Permissions**: Admin only

**Request Example**:
```json
{
  "sport_event": "3fa85f64-5717-4562-b3fc-2c963f66afa7"
}
```

**Response Example**: Same as Retrieve Leaderboard with empty entries array

### Update Leaderboard

Updates leaderboard properties (not entries).

**Endpoint**: `PUT /api/leaderboards/{id}/`

**Parameters**:
- `id` (path parameter): Leaderboard ID (UUID)

**Permissions**: Admin only

**Request Example**:
```json
{
  "is_final": true
}
```

**Response Example**: Same as Retrieve Leaderboard with updated fields

### Delete Leaderboard

Deletes a leaderboard and all its entries.

**Endpoint**: `DELETE /api/leaderboards/{id}/`

**Parameters**:
- `id` (path parameter): Leaderboard ID (UUID)

**Permissions**: Admin only

**Response**: HTTP 204 No Content

### Calculate Leaderboard

Recalculates a leaderboard based on current game results.

**Endpoint**: `POST /api/leaderboards/{id}/calculate/`

**Parameters**:
- `id` (path parameter): Leaderboard ID (UUID)

**Permissions**: Admin only

**Response Example**: Same as Retrieve Leaderboard with updated entries

### Finalize Leaderboard

Marks a leaderboard as final, indicating the tournament is complete.

**Endpoint**: `POST /api/leaderboards/{id}/finalize/`

**Parameters**:
- `id` (path parameter): Leaderboard ID (UUID)

**Permissions**: Admin only

**Response Example**: Same as Retrieve Leaderboard with `is_final` set to `true`

### Team Leaderboards

Gets all leaderboard entries for a specific team across different sport events.

**Endpoint**: `GET /api/leaderboards/team/{team_id}/`

**Parameters**:
- `team_id` (path parameter): Team ID (UUID)

**Permissions**: Public access

**Response Example**:
```json
[
  {
    "sport_event_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
    "sport_event_name": "Annual Football Tournament 2025",
    "position": 1,
    "played": 5,
    "won": 4,
    "drawn": 0,
    "lost": 1,
    "points": 12,
    "goals_for": 12,
    "goals_against": 5,
    "goal_difference": 7,
    "is_final": false
  },
  {
    "sport_event_id": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
    "sport_event_name": "Summer Cup 2024",
    "position": 3,
    "played": 4,
    "won": 2,
    "drawn": 1,
    "lost": 1,
    "points": 7,
    "goals_for": 8,
    "goals_against": 7,
    "goal_difference": 1,
    "is_final": true
  }
]
```

## Leaderboard Entry Endpoints

### List Leaderboard Entries

Retrieves a paginated list of all leaderboard entries with filtering options.

**Endpoint**: `GET /api/leaderboards/entries/`

**Parameters**:
- `leaderboard` (optional): Filter by leaderboard ID
- `team` (optional): Filter by team ID
- `position` (optional): Filter by position
- `ordering` (optional): Order by field (e.g., `position`, `-points`)

**Permissions**: Public access

**Response Example**:
```json
{
  "count": 12,
  "next": "http://example.com/api/leaderboards/entries/?page=2",
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "team_name": "Eagles",
      "position": 1,
      "played": 5,
      "won": 4,
      "drawn": 0,
      "lost": 1,
      "points": 12,
      "goals_for": 12,
      "goals_against": 5,
      "goal_difference": 7,
      "clean_sheets": 2,
      "yellow_cards": 3,
      "red_cards": 0
    }
  ]
}
```

### Retrieve Leaderboard Entry

Gets detailed information about a specific leaderboard entry.

**Endpoint**: `GET /api/leaderboards/entries/{id}/`

**Parameters**:
- `id` (path parameter): Leaderboard Entry ID (UUID)

**Permissions**: Public access

**Response Example**: Same as an individual entry in List Leaderboard Entries