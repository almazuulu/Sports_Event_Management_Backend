# Score API Documentation

This document provides comprehensive information about the Score API endpoints for the Sports Event Management system, including descriptions, example requests, and responses.

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Score Endpoints](#score-endpoints)
   - [List Scores](#list-scores)
   - [Create Score](#create-score)
   - [Retrieve Score](#retrieve-score)
   - [Update Score](#update-score)
   - [Partial Update Score](#partial-update-score)
   - [Delete Score](#delete-score)
   - [Verify Score](#verify-score)
   - [Public Scores](#public-scores)
   - [Live Scores](#live-scores)
   - [Scorekeeper's Assigned Games](#scorekeepers-assigned-games)
   - [Event Leaderboard](#event-leaderboard)
4. [Score Detail Endpoints](#score-detail-endpoints)
   - [List Score Details](#list-score-details)
   - [Create Score Detail](#create-score-detail)
   - [Retrieve Score Detail](#retrieve-score-detail)
   - [Update Score Detail](#update-score-detail)
   - [Partial Update Score Detail](#partial-update-score-detail)
   - [Delete Score Detail](#delete-score-detail)
   - [Score Details by Score](#score-details-by-score)
5. [Nested Score Detail Endpoints](#nested-score-detail-endpoints)
   - [List Score Details for Score](#list-score-details-for-score)
   - [Create Score Detail for Score](#create-score-detail-for-score)
   - [Retrieve Score Detail for Score](#retrieve-score-detail-for-score)
   - [Update Score Detail for Score](#update-score-detail-for-score)
   - [Partial Update Score Detail for Score](#partial-update-score-detail-for-score)
   - [Delete Score Detail for Score](#delete-score-detail-for-score)

## Introduction

The Score API provides endpoints for managing game scores and detailed scoring events (goals, points, etc.) within the Multi-Sport Event Management System. This API allows scorekeepers to track live scores, administrators to verify completed games, and provides public access to game results and leaderboards.

## Authentication

Most endpoints require authentication using JWT (JSON Web Token). Include the token in the Authorization header:

```
Authorization: Bearer {your_token}
```

Different endpoints have different permission requirements:
- **Admin Users**: Can perform all operations and verify scores
- **Scorekeepers**: Can update scores and add scoring events for games they are assigned to
- **Team Managers/Captains**: Can view scores related to their teams
- **Public Users**: Can view public score information and leaderboards

## Score Endpoints

### List Scores

Retrieves a paginated list of all scores with filtering options.

**Endpoint**: `GET /api/scores/scores/`

**Parameters**:
- `game` (optional): Filter by game ID
- `status` (optional): Filter by score status (`pending`, `in_progress`, `completed`, `cancelled`)
- `verification_status` (optional): Filter by verification status (`unverified`, `pending_verification`, `verified`, `disputed`)
- `ordering` (optional): Order by field (e.g., `created_at`, `-created_at`)

**Permissions**: Authenticated users

**Response Example**:
```json
{
  "count": 15,
  "next": "http://example.com/api/scores/scores/?page=2",
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "game": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
      "game_name": "Football Match 1 - Group Stage",
      "team1": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
      "team1_name": "Eagles",
      "team2": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "team2_name": "Falcons",
      "status": "completed",
      "final_score_team1": 3,
      "final_score_team2": 2,
      "goals_for_team1": 3,
      "goals_against_team1": 2,
      "goals_for_team2": 2,
      "goals_against_team2": 3,
      "goal_difference_team1": 1,
      "goal_difference_team2": -1,
      "time_elapsed": "90",
      "winner": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
      "winner_name": "Eagles",
      "is_draw": false,
      "notes": "Exciting match with last-minute goal",
      "verification_status": "verified",
      "scorekeeper": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa1",
        "full_name": "John Smith"
      },
      "created_at": "2025-03-10T12:30:00Z",
      "updated_at": "2025-03-10T14:45:00Z",
      "score_details": [
        {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afb1",
          "score": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "team": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
          "team_name": "Eagles",
          "player": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
          "player_name": "Michael Johnson",
          "points": 1,
          "time_occurred": "00:15:30",
          "minute": 15,
          "period": "First Half",
          "event_type": "goal"
        }
      ]
    }
  ]
}
```

### Create Score

Creates a new score record for a game.

**Endpoint**: `POST /api/scores/scores/`

**Permissions**: Admins or scorekeepers

**Request Example**:
```json
{
  "game": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
  "status": "pending",
  "scorekeeper": "3fa85f64-5717-4562-b3fc-2c963f66afa1"
}
```

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "game": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
  "game_name": "Football Match 1 - Group Stage",
  "team1": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
  "team1_name": "Eagles",
  "team2": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
  "team2_name": "Falcons",
  "status": "pending",
  "final_score_team1": 0,
  "final_score_team2": 0,
  "goals_for_team1": 0,
  "goals_against_team1": 0,
  "goals_for_team2": 0,
  "goals_against_team2": 0,
  "goal_difference_team1": 0,
  "goal_difference_team2": 0,
  "time_elapsed": "",
  "winner": null,
  "winner_name": null,
  "is_draw": false,
  "notes": "",
  "verification_status": "unverified",
  "scorekeeper": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa1",
    "full_name": "John Smith"
  },
  "created_at": "2025-03-10T12:30:00Z",
  "updated_at": "2025-03-10T12:30:00Z",
  "score_details": []
}
```

### Retrieve Score

Retrieves detailed information about a specific score.

**Endpoint**: `GET /api/scores/scores/{id}/`

**Parameters**:
- `id` (path parameter): Score ID (UUID)

**Permissions**: Authenticated users

**Response Example**: Same as in List Scores

### Update Score

Updates all details of an existing score.

**Endpoint**: `PUT /api/scores/scores/{id}/`

**Parameters**:
- `id` (path parameter): Score ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Request Example**:
```json
{
  "status": "in_progress",
  "final_score_team1": 1,
  "final_score_team2": 0,
  "goals_for_team1": 1,
  "goals_against_team1": 0,
  "goals_for_team2": 0,
  "goals_against_team2": 1,
  "time_elapsed": "35",
  "notes": "Home team leads at 35 minutes"
}
```

**Response Example**: Same as Retrieve Score with updated values

### Partial Update Score

Updates specific fields of an existing score.

**Endpoint**: `PATCH /api/scores/scores/{id}/`

**Parameters**:
- `id` (path parameter): Score ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Request Example**:
```json
{
  "status": "completed",
  "final_score_team1": 3,
  "final_score_team2": 2,
  "time_elapsed": "90+3"
}
```

**Response Example**: Same as Retrieve Score with updated values

### Delete Score

Removes a score record from the system.

**Endpoint**: `DELETE /api/scores/scores/{id}/`

**Parameters**:
- `id` (path parameter): Score ID (UUID)

**Permissions**: Admin or scorekeeper with manage scores permission

**Response**: HTTP 204 No Content

### Verify Score

Verifies a completed score by an administrator.

**Endpoint**: `PATCH /api/scores/scores/{id}/verify/`

**Parameters**:
- `id` (path parameter): Score ID (UUID)

**Permissions**: Admin only

**Request Example**:
```json
{
  "verified": true,
  "verification_status": "verified",
  "notes": "Verified after checking with both team captains"
}
```

**Response Example**: Same as Retrieve Score with verification information updated

### Public Scores

Gets a list of scores for public display.

**Endpoint**: `GET /api/scores/scores/public/`

**Parameters**:
- `sport_event` (optional): Filter by sport event ID
- `team` (optional): Filter by team ID
- `status` (optional): Filter by status (e.g., `completed`)

**Permissions**: Public access

**Response Example**:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "game_name": "Football Match 1 - Group Stage",
      "event_name": "Annual Sports Tournament 2025",
      "sport_type": "football",
      "sport_name": "Football",
      "team1_name": "Eagles",
      "team2_name": "Falcons",
      "final_score_team1": 3,
      "final_score_team2": 2,
      "goals_for_team1": 3,
      "goals_against_team1": 2,
      "goal_difference_team1": 1,
      "goals_for_team2": 2,
      "goals_against_team2": 3,
      "goal_difference_team2": -1,
      "status": "completed",
      "status_display": "Completed",
      "winner_name": "Eagles",
      "is_draw": false
    }
  ]
}
```

### Live Scores

Gets a list of currently active game scores with live updates.

**Endpoint**: `GET /api/scores/scores/live/`

**Parameters**:
- `sport_event` (optional): Filter by sport event ID

**Permissions**: Public access

**Response Example**:
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "game_name": "Football Match 1 - Group Stage",
    "match_day": "Week 3",
    "team1_name": "Eagles",
    "team2_name": "Falcons",
    "location": "Olympic Stadium",
    "scheduled_start": "2025-03-10T14:00:00Z",
    "status": "in_progress",
    "status_display": "In Progress",
    "time_elapsed": "60",
    "final_score_team1": 2,
    "final_score_team2": 1,
    "score_updates": [
      {
        "team": "Eagles",
        "player": "Michael Johnson",
        "assisted_by": "David Smith",
        "points": 1,
        "event_type": "goal",
        "time": "14:15:30",
        "minute": 55,
        "period": "Second Half",
        "description": "Header from corner kick"
      },
      {
        "team": "Eagles",
        "player": "Marcus Brown",
        "assisted_by": null,
        "points": 1,
        "event_type": "penalty",
        "time": "14:02:15",
        "minute": 42,
        "period": "First Half",
        "description": "Penalty kick after foul in the box"
      },
      {
        "team": "Falcons",
        "player": "Alex Johnson",
        "assisted_by": "Chris Williams",
        "points": 1,
        "event_type": "goal",
        "time": "13:35:12",
        "minute": 15,
        "period": "First Half",
        "description": "Shot from outside the box"
      }
    ]
  }
]
```

### Scorekeeper's Assigned Games

Gets scores for games assigned to the current scorekeeper.

**Endpoint**: `GET /api/scores/scores/my-assignments/`

**Permissions**: Scorekeeper only

**Response Example**:
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "game": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
      "game_name": "Football Match 1 - Group Stage",
      "team1": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
      "team1_name": "Eagles",
      "team2": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "team2_name": "Falcons",
      "status": "scheduled",
      "final_score_team1": 0,
      "final_score_team2": 0,
      "time_elapsed": "",
      "verification_status": "unverified",
      "created_at": "2025-03-10T12:30:00Z",
      "updated_at": "2025-03-10T12:30:00Z"
    }
  ]
}
```

### Event Leaderboard

Gets a leaderboard for a specific sport event.

**Endpoint**: `GET /api/scores/scores/leaderboard/`

**Parameters**:
- `sport_event` (required): Sport event ID

**Permissions**: Public access

**Response Example**:
```json
[
  {
    "team_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
    "team_name": "Eagles",
    "played": 5,
    "won": 4,
    "drawn": 0,
    "lost": 1,
    "goals_for": 12,
    "goals_against": 5,
    "goal_difference": 7,
    "points": 12
  },
  {
    "team_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    "team_name": "Falcons",
    "played": 5,
    "won": 3,
    "drawn": 1,
    "lost": 1,
    "goals_for": 10,
    "goals_against": 6,
    "goal_difference": 4,
    "points": 10
  }
]
```

## Score Detail Endpoints

Score details represent individual scoring events within a game (e.g., goals, points, baskets).

### List Score Details

Retrieves a paginated list of all scoring events with filtering options.

**Endpoint**: `GET /api/scores/score-details/`

**Parameters**:
- `score` (optional): Filter by score ID
- `team` (optional): Filter by team ID
- `player` (optional): Filter by player ID
- `event_type` (optional): Filter by event type (e.g., `goal`, `penalty`, `basket`)
- `ordering` (optional): Order by field (e.g., `time_occurred`, `minute`)

**Permissions**: Authenticated users

**Response Example**:
```json
{
  "count": 25,
  "next": "http://example.com/api/scores/score-details/?page=2",
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afb1",
      "score": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
      "team_name": "Eagles",
      "player": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
      "player_name": "Michael Johnson",
      "assisted_by": "3fa85f64-5717-4562-b3fc-2c963f66afb3",
      "assisted_by_name": "David Smith",
      "points": 1,
      "event_type": "goal",
      "time_occurred": "00:15:30",
      "minute": 15,
      "period": "First Half",
      "description": "Goal from left wing",
      "video_url": "https://example.com/videos/goal-12345"
    }
  ]
}
```

### Create Score Detail

Creates a new scoring event for a game.

**Endpoint**: `POST /api/scores/score-details/`

**Permissions**: Assigned scorekeeper or admin

**Request Example**:
```json
{
  "team": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
  "player": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
  "assisted_by": "3fa85f64-5717-4562-b3fc-2c963f66afb3",
  "points": 1,
  "event_type": "goal",
  "time_occurred": "00:15:30",
  "minute": 15,
  "period": "First Half",
  "description": "Goal from left wing"
}
```

**Response Example**:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afb1",
  "score": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "team": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
  "team_name": "Eagles",
  "player": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
  "player_name": "Michael Johnson",
  "assisted_by": "3fa85f64-5717-4562-b3fc-2c963f66afb3",
  "assisted_by_name": "David Smith",
  "points": 1,
  "event_type": "goal",
  "time_occurred": "00:15:30",
  "minute": 15,
  "period": "First Half",
  "description": "Goal from left wing",
  "video_url": null
}
```

### Retrieve Score Detail

Retrieves detailed information about a specific scoring event.

**Endpoint**: `GET /api/scores/score-details/{id}/`

**Parameters**:
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Authenticated users

**Response Example**: Same as in List Score Details

### Update Score Detail

Updates all details of an existing scoring event.

**Endpoint**: `PUT /api/scores/score-details/{id}/`

**Parameters**:
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Request Example**:
```json
{
  "team": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
  "player": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
  "assisted_by": "3fa85f64-5717-4562-b3fc-2c963f66afb3",
  "points": 1,
  "event_type": "free_kick",
  "time_occurred": "00:15:30",
  "minute": 15,
  "period": "First Half",
  "description": "Updated: Free kick goal from 25 yards"
}
```

**Response Example**: Same as Retrieve Score Detail with updated values

### Partial Update Score Detail

Updates specific fields of an existing scoring event.

**Endpoint**: `PATCH /api/scores/score-details/{id}/`

**Parameters**:
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Request Example**:
```json
{
  "event_type": "free_kick",
  "description": "Updated: Free kick goal from 25 yards"
}
```

**Response Example**: Same as Retrieve Score Detail with updated values

### Delete Score Detail

Removes a scoring event from the system.

**Endpoint**: `DELETE /api/scores/score-details/{id}/`

**Parameters**:
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Response**: HTTP 204 No Content

### Score Details by Score

Gets all scoring events for a specific game score.

**Endpoint**: `GET /api/scores/score-details/by-score/{score_id}/`

**Parameters**:
- `score_id` (path parameter): Score ID (UUID)

**Permissions**: Authenticated users

**Response Example**:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afb1",
      "score": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
      "team_name": "Eagles",
      "player": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
      "player_name": "Michael Johnson",
      "assisted_by": "3fa85f64-5717-4562-b3fc-2c963f66afb3",
      "assisted_by_name": "David Smith",
      "points": 1,
      "event_type": "goal",
      "time_occurred": "00:15:30",
      "minute": 15,
      "period": "First Half",
      "description": "Goal from left wing",
      "video_url": null
    },
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afb4",
      "score": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "team": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
      "team_name": "Falcons",
      "player": "3fa85f64-5717-4562-b3fc-2c963f66afb5",
      "player_name": "Alex Johnson",
      "assisted_by": null,
      "assisted_by_name": null,
      "points": 1,
      "event_type": "goal",
      "time_occurred": "00:35:15",
      "minute": 35,
      "period": "First Half",
      "description": "Equalizer from counter-attack",
      "video_url": null
    }
  ]
}
```

## Nested Score Detail Endpoints

These endpoints allow you to manage score details as a nested resource under a specific score.

### List Score Details for Score

Retrieves all scoring events for a specific score.

**Endpoint**: `GET /api/scores/scores/{score_pk}/details/`

**Parameters**:
- `score_pk` (path parameter): Score ID (UUID)

**Permissions**: Authenticated users

**Response Example**: Same format as [Score Details by Score](#score-details-by-score)

### Create Score Detail for Score

Creates a new scoring event for a specific score.

**Endpoint**: `POST /api/scores/scores/{score_pk}/details/`

**Parameters**:
- `score_pk` (path parameter): Score ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Request Example**:
```json
{
  "team": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
  "player": "3fa85f64-5717-4562-b3fc-2c963f66afb2",
  "assisted_by": "3fa85f64-5717-4562-b3fc-2c963f66afb3",
  "points": 1,
  "event_type": "goal",
  "time_occurred": "00:15:30",
  "minute": 15,
  "period": "First Half",
  "description": "Goal from left wing"
}
```

**Response Example**: Same as [Create Score Detail](#create-score-detail)

### Retrieve Score Detail for Score

Retrieves a specific scoring event for a specific score.

**Endpoint**: `GET /api/scores/scores/{score_pk}/details/{id}/`

**Parameters**:
- `score_pk` (path parameter): Score ID (UUID)
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Authenticated users

**Response Example**: Same as [Retrieve Score Detail](#retrieve-score-detail)

### Update Score Detail for Score

Updates all details of a specific scoring event for a specific score.

**Endpoint**: `PUT /api/scores/scores/{score_pk}/details/{id}/`

**Parameters**:
- `score_pk` (path parameter): Score ID (UUID)
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Request Example**: Same as [Update Score Detail](#update-score-detail)

**Response Example**: Same as [Retrieve Score Detail](#retrieve-score-detail) with updated values

### Partial Update Score Detail for Score

Updates specific fields of a scoring event for a specific score.

**Endpoint**: `PATCH /api/scores/scores/{score_pk}/details/{id}/`

**Parameters**:
- `score_pk` (path parameter): Score ID (UUID)
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Request Example**: Same as [Partial Update Score Detail](#partial-update-score-detail)

**Response Example**: Same as [Retrieve Score Detail](#retrieve-score-detail) with updated values

### Delete Score Detail for Score

Removes a scoring event from a specific score.

**Endpoint**: `DELETE /api/scores/scores/{score_pk}/details/{id}/`

**Parameters**:
- `score_pk` (path parameter): Score ID (UUID)
- `id` (path parameter): Score Detail ID (UUID)

**Permissions**: Assigned scorekeeper or admin

**Response**: HTTP 204 No Content
