# PRD for Backend

## Overview
The backend of Cookero-app is built using FastAPI. It should be a RESTful API that allows for creating, reading, updating, and deleting recipes.

## Product Goals
Initial plan is self-use through a web browser. Future plans include mobile app and desktop app.

## Data Model
The data model should be based on the following JSON schema:
```json
{
    "id": int,
    "name": str,
    "ingredients": [
        {
            "name": str,
            "amount": str
        }
    ],
    "instructions": str
}
```

## Functional Requirements
1. The app should allow for multiple users to have their own personal recipes, plans, and shopping lists.
2. A user shoudl be able to create, edit, and delete recipes.
3. A user should be able to view the ingredients for a recipe.
4. A user should be able to view the instructions for a recipe.

## APIs
The app should have the following APIs:
1. Sign up
2. Sign in
3. Create a recipe
4. Read a recipe
5. Update a recipe
6. Delete a recipe
7. List all recipes
8. List recipes by ingredients

## Non-Functional Requirements
1. The app should be fast and responsive.
2. The app should be secure.
3. The app should be easy to use.
4. The app should be easy to debug.
5. The app should be easy to maintain.
6. The app should be easy to scale.
7. The app should be easy to test.

## Success Metrics and KPIs
1. Number of users
2. Number of recipes
3. Number of plans
4. Number of shopping lists
5. Time to create a recipe
6. Time to read a recipe
7. Time to update a recipe
8. Time to delete a recipe
9. Time to list all recipes
10. Time to list recipes by ingredients

## Roadmap
1. Create simple backend with support for User Authentication and CRUD for recipes.
2. add support for indicating ingredients in recipes
3. add support for reverse recipe search based on ingredients