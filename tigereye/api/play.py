from flask import request, json
import redis
from tigereye.api import ApiView
from tigereye.extensions.validator import Validator
from tigereye.models.seat import PlaySeat, SeatType

r = redis.Redis()

class PlayView(ApiView):

    @Validator(pid=int)
    def seats(self):
        pid = request.params['pid']
        key = 'play_seats_%s' % pid
        ps = r.lrange(key, 0 ,-1)
        ps = [json.loads(p.decode('utf-8')) for p in ps]
        if not ps:
            ps = PlaySeat.query.filter(
                PlaySeat.pid == pid,
                PlaySeat.seat_type != SeatType.road.value
            ).all()
            r.lpush(key, *[json.dumps(p) for p in ps])
        return ps