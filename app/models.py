import re
import json


class User:
    def __init__(self, id, first_name, second_name, email, sport, contests):
        self.id = id
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.sport = sport
        self.contests = contests

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False


class Contests:
    def __init__(self, id, name, sport, participants, winner=None, status="STARTED"):
        self.id = id
        self.name = name
        self.sport = sport
        self.status = status
        self.participants = participants
        self.winner = winner

    def finish(self, winner):
        self.winner = winner
        self.status = "FINISHED"

    def get_info(self):
        data = {
            "id": self.id,
            "name": self.name,
            "sport": self.sport,
            "status": self.status,
            "participants": self.participants,
            "winner": self.winner,
        }

        return data
