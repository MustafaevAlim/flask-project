from app import app
from app import USERS, CONTESTS
from http import HTTPStatus
from flask import request, Response, url_for
from app import models
from matplotlib import pyplot as plt
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

    user = models.User(id, first_name, second_name, email, sport)
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
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
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
    id_participants = data["participants"]
    participants = []
    for i in id_participants:
        try:
            user = USERS[i]
            user.contests.append(id)
            participants.append(user)
        except IndexError:
            response = (
                f"Такого участника нет. Список доступных для этого соревнования: <br>"
                f"""{'<br>'.join([str(user.id) + ") " + user.first_name + user.second_name for user in USERS])}"""
            )
            return Response(
                response,
                status=HTTPStatus.BAD_REQUEST,
            )

    contest = models.Contests(id, name, sport, participants)
    CONTESTS.append(contest)
    if not contest.valid_participants(participants):
        return Response(
            response=f"Участники не могут учавствовать в соревновании по этому виду спорта",
            status=HTTPStatus.BAD_REQUEST,
        )

    body = {
        "id": id,
        "name": name,
        "sport": sport,
        "status": contest.status,
        "participants": id_participants,
        "winner": contest.winner,
    }

    response = Response(
        response=json.dumps(body),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response


@app.get("/contest/<int:contest_id>")
def get_contest_by_id(contest_id):
    if contest_id < 0 or contest_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    contest = CONTESTS[contest_id]
    body = {
        "id": contest_id,
        "name": contest.name,
        "sport": contest.sport,
        "status": contest.status,
        "participants": contest.participants,
        "winner": contest.winner,
    }

    response = Response(
        response=json.dumps(body),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response


@app.post("/contest/<int:contest_id>/finish")
def finish_contest(contest_id):
    contest = CONTESTS[contest_id]
    data = request.get_json()
    winner = data["winner"]
    contest.finish(winner)

    body = {
        "id": contest_id,
        "name": contest.name,
        "sport": contest.sport,
        "status": contest.status,
        "participants": contest.participants,
        "winner": winner,
    }

    response = Response(
        response=json.dumps(body),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response


@app.get("/users/<int:user_id>/contests")
def get_user_contests(user_id):
    user = USERS[user_id]
    contest = user.contests
    data = [CONTESTS[i].get_info() for i in contest]
    body = {
        "contest": data,
    }

    response = Response(
        response=json.dumps(body),
        status=HTTPStatus.OK,
        mimetype="application.json",
    )

    return response


@app.get("/users/leaderboard")
def get_leaderboard():
    data = request.get_json()
    users = [user.get_info() for user in USERS]
    if data["type"] == "list":
        if data["sort"] == "asc":
            users = sorted(USERS)
        elif data["sort"] == "desc":
            users = sorted(USERS, reverse=True)

        users = {"users": [user.get_info() for user in users]}
        return Response(
            response=json.dumps(users),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )
    elif data["type"] == "graph":
        fig, ax = plt.subplots()
        name = [
            f'{user["first_name"] + user["second_name"] + str(user["id"])}'
            for user in users
        ]
        contests = [len(user["contests"]) for user in users]
        ax.bar(name, contests)
        ax.set_ylabel("Кол-во соревнований")
        plt.savefig("app/static/leaderboard.png")
        return Response(
            response=(f'<img src={url_for("static", filename="leaderboard.png")}/>'),
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    else:
        return Response(status=HTTPStatus.NOT_FOUND)
