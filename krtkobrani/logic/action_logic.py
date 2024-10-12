import enum
from datetime import datetime, timedelta

from krtkobrani.db_models import Site, Action, Team
from krtkobrani.db import db
from krtkobrani.endpoints.admin import admin
from krtkobrani.endpoints.base import teams
from krtkobrani.logic.errors import BadState, TooSoon, NoNextSite


class ActionStates(enum.Enum):
    UNKNOWN = 0
    ENTER = 1
    HELP_1 = 2
    HELP_2 = 3
    EXIT = 4
    DEAD = 5


def sanitize_string(the_string):
    the_string = ''.join(the_string.split()) # remove all whitespaces
    return the_string.lower() # to lower case


def start_game():
    all_teams = db.session.query(Team).all()
    first_site = db.session.query(Site).filter_by(site_number=1).first()
    start_time = datetime.utcnow()
    for team in all_teams:
        for team in all_teams:
            # Check if an action for this team already exists
        existing_action = db.session.query(Action).filter_by(team_id=team.id).first()
    if existing_action:

        new_action = Action(
            site_id=first_site.id,
            team_id=team.id,
            action_state=ActionStates.ENTER.value,
            timestamp=start_time,
            guess="",
            success=True
        )
        db.session.add(new_action)
    db.session.commit()




def try_to_solve(team_id, guess):
    current_site_id = (db.session.query(Action.site_id).filter_by(team_id=team_id, action_state=ActionStates.ENTER.value,
                       success=True).order_by(Action.site_id.desc()).first())[0]
    current_site = db.session.query(Site).filter_by(id=current_site_id).first()
    sanitized_guess = sanitize_string(guess)
    if sanitized_guess == sanitize_string(current_site.exit_pass):
        new_action = Action(
            site_id=current_site_id,
            team_id=team_id,
            action_state=ActionStates.EXIT.value,
            timestamp=datetime.utcnow(),
            guess=sanitized_guess,
            success=True
        )
    else:
        new_action = Action(
            site_id=current_site_id,
            team_id=team_id,
            action_state=ActionStates.EXIT.value,
            timestamp=datetime.utcnow(),
            guess=sanitized_guess,
            success=False
        )
    db.session.add(new_action)
    db.session.commit()
    # return new_action


def try_to_enter(team_id, guess):
    current_site_id = (db.session.query(Action.site_id).filter(Action.team_id==team_id)
                       .filter((Action.action_state == ActionStates.EXIT.value) | (Action.action_state == ActionStates.DEAD.value))
                       .filter(Action.success==True)
                       .order_by(Action.site_id.desc()).first())[0]
    current_site_number = db.session.query(Site.site_number).filter_by(id=current_site_id).first()[0]
    current_site_number += 1
    current_site = db.session.query(Site).filter_by(site_number=current_site_number).first()
    if not current_site:
        raise NoNextSite(f"There is no site number {current_site_number}", current_site_number)
    sanitized_guess = sanitize_string(guess)
    if sanitized_guess == sanitize_string(current_site.entry_pass):
        new_action = Action(
            site_id=current_site.id,
            team_id=team_id,
            action_state=ActionStates.ENTER.value,
            timestamp=datetime.utcnow(),
            guess=sanitized_guess,
            success=True
        )
    else:
        new_action = Action(
            site_id=current_site.id,
            team_id=team_id,
            action_state=ActionStates.ENTER.value,
            timestamp=datetime.utcnow(),
            guess=sanitized_guess,
            success=False
        )
    db.session.add(new_action)
    db.session.commit()
    # return new_action


def ask_for_help(team_id):
    last_action = (db.session.query(Action).filter_by(team_id=team_id, success=True)
                   .order_by(Action.id.desc()).first())
    current_site = db.session.query(Site).filter_by(id=last_action.site_id).first()
    if last_action.action_state == ActionStates.ENTER.value:
        next_action = ActionStates.HELP_1.value
        minutes_since_enter = current_site.help_1_time_minutes
    elif last_action.action_state == ActionStates.HELP_1.value:
        next_action = ActionStates.HELP_2.value
        minutes_since_enter = current_site.help_2_time_minutes
    elif last_action.action_state == ActionStates.HELP_2.value:
        next_action = ActionStates.DEAD.value
        minutes_since_enter = current_site.dead_time_minutes
    else:
        raise BadState(f"Cant ask for help in state {last_action.action_state}", last_action.action_state)

    now = datetime.utcnow()
    entry_action = db.session.query(Action).filter_by(site_id=current_site.id, action_state=ActionStates.ENTER.value,
                                                      success=True).first()

    if (next_time := entry_action.timestamp + timedelta(minutes=minutes_since_enter)) > now:
        raise TooSoon("Can't get help yet", next_time)

    new_action = Action(
        site_id=last_action.site_id,
        team_id=team_id,
        action_state=next_action,
        timestamp=now,
        guess="",
        success=True
    )
    db.session.add(new_action)
    db.session.commit()
    # return new_action
