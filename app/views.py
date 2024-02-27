from app import app
from app import USERS, CONTESTS
from http import HTTPStatus
from flask import request, Response
from app import models
import json


@app.post("/users/create")
def user_create():
    data = request.get_json()
    first_name = data["first_name"]
    second_name = data["second_name"]
    email = data["email"]
    sport = data["sport"]
    id = len(USERS)

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(id, first_name, second_name, email, sport, contests=[])
    USERS.append(user)

    body = dict()
    body["id"] = id
    body["first_name"] = first_name
    body["second_name"] = second_name
    body["email"] = email
    body["contests"] = CONTESTS

    response = Response(
        response=json.dumps(body),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response


@app.get("/users/<int:user_id>")
def get_user_id(user_id):
    user = USERS[user_id]
    body = {
        "id": user.id,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "email": user.email,
        "contests": user.contests,
    }

    response = Response(
        response=json.dumps(body),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response


@app.post("/contest/create")
def contest_create():
    data = request.get_json()
    id = len(CONTESTS)
    name = data["name"]
    sport = data["sport"]
    participants = data["participants"]

    contest = models.Contests(id, name, sport, participants)
    CONTESTS.append(contest)

    body = {
        "id": id,
        "name": name,
        "sport": sport,
        "status": contest.status,
        "participants": participants,
        "winner": contest.winner,
    }

    response = Response(
        response=json.dumps(body),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response
