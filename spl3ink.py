import dataclasses
import enum

import pendulum
import requests as req


class MatchType(str, enum.Enum):
    REGULAR = 'regular'
    X = 'X'
    CHALLENGE = 'challenge'
    OPEN = 'open'


@dataclasses.dataclass
class MatchInfo:
    match_type: MatchType
    start_datetime: str
    end_datetime: str
    vs_rule: str
    maps: list[str]


@dataclasses.dataclass
class TotalMatchInfo:
    regular: MatchInfo
    x: MatchInfo
    challenge: MatchInfo
    open: MatchInfo


TOTAL_MATCH_INFO = None


def make_info(match_type: MatchType, schedule_dict: dict, locale_dict: dict) -> MatchInfo:
    if match_type == MatchType.REGULAR:
        starttime = schedule_dict['data']['regularSchedules']['nodes'][0]['startTime']
        endtime =  schedule_dict['data']['regularSchedules']['nodes'][0]['endTime']
        settings = schedule_dict['data']['regularSchedules']['nodes'][0]['regularMatchSetting']
    elif match_type == MatchType.X:
        starttime = schedule_dict['data']['xSchedules']['nodes'][0]['startTime']
        endtime =  schedule_dict['data']['xSchedules']['nodes'][0]['endTime']
        settings = schedule_dict['data']['xSchedules']['nodes'][0]['xMatchSetting']
    elif match_type == MatchType.CHALLENGE:
        starttime = schedule_dict['data']['bankaraSchedules']['nodes'][0]['startTime']
        endtime =  schedule_dict['data']['bankaraSchedules']['nodes'][0]['endTime']
        settings = schedule_dict['data']['bankaraSchedules']['nodes'][0]['bankaraMatchSettings'][0]
    elif match_type == MatchType.OPEN:
        starttime = schedule_dict['data']['bankaraSchedules']['nodes'][0]['startTime']
        endtime =  schedule_dict['data']['bankaraSchedules']['nodes'][0]['endTime']
        settings = schedule_dict['data']['bankaraSchedules']['nodes'][0]['bankaraMatchSettings'][1]
    starttime_str = pendulum.parse(starttime).in_tz('Asia/Seoul').format('LLL', locale='ko')
    endtime_str = pendulum.parse(endtime).in_tz('Asia/Seoul').format('LLL', locale='ko')
    vs_rule = locale_dict['rules'][settings['vsRule']['id']]['name']
    maps = [locale_dict['stages'][settings['vsStages'][0]['id']]['name'], locale_dict['stages'][settings['vsStages'][1]['id']]['name']]

    return MatchInfo(
        match_type=match_type,
        start_datetime=starttime_str,
        end_datetime=endtime_str,
        vs_rule=vs_rule,
        maps=maps
    )


def get_match_infos() -> TotalMatchInfo:
    global TOTAL_MATCH_INFO
    if TOTAL_MATCH_INFO is None:
        schedule_url = 'https://splatoon3.ink/data/schedules.json'
        locale_url = 'https://splatoon3.ink/data/locale/ko-KR.json'
        schedule_dict = req.get(schedule_url).json()
        locale_dict = req.get(locale_url).json()

        regular = make_info(MatchType.REGULAR, schedule_dict, locale_dict)
        x = make_info(MatchType.X, schedule_dict, locale_dict)
        challenge = make_info(MatchType.CHALLENGE, schedule_dict, locale_dict)
        open = make_info(MatchType.OPEN, schedule_dict, locale_dict)

        TOTAL_MATCH_INFO = TotalMatchInfo(regular=regular, x=x, challenge=challenge, open=open)
    return TOTAL_MATCH_INFO


if __name__ == "__main__":
    print(get_match_infos().regular)
    print(get_match_infos().x)
    print(get_match_infos().open)
    print(get_match_infos().challenge)