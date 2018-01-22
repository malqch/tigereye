from datetime import datetime
from enum import Enum, unique
from sqlalchemy import text
from tigereye.models import db, Model

@unique
class SeatStatus(Enum):
    """正常状态，可购买"""
    ok = 0
    """已锁定"""
    locked = 1
    """已售出"""
    sold = 2
    """已打票"""
    printed = 3
    """已预订"""
    booked = 9
    """维修中"""
    repair = 99


@unique
class SeatType(Enum):
    """过道"""
    road = 0
    """单人"""
    single = 1
    """双人"""
    couple = 2
    """保留座位"""
    reserve = 3
    """残疾专座"""
    for_disable = 4
    """VIP专座"""
    vip = 5
    """震动座椅"""
    shake = 6

class Seat(db.Model, Model):
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    row = db.Column(db.String(16))
    column = db.Column(db.String(16))

    area = db.Column(db.String(16))
    seat_type = db.Column(db.String(16))
    love_seats = db.Column(db.String(16))
    status = db.Column(db.Integer, default=0, nullable=False, index=True)

"""
    

"""

class PlaySeat(db.Model, Model):
    psid = db.Column(db.Integer, primary_key=True)
    orderno = db.Column(db.String(32), index=True)
    cid = db.Column(db.Integer)
    hid = db.Column(db.Integer)

    sid = db.Column(db.Integer)
    pid = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    row = db.Column(db.String(16))
    column = db.Column(db.String(16))
    area = db.Column(db.String(16))
    seat_type = db.Column(db.String(16))
    love_seats = db.Column(db.String(16))
    status = db.Column(db.Integer, default=0, nullable=False, index=True)

    lock_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))

    def copy(self, seat):
        self.sid = seat.sid
        self.cid = seat.cid
        self.hid = seat.hid
        self.x = seat.x
        self.y = seat.y
        self.row = seat.row
        self.column = seat.column
        self.area = seat.area
        self.seat_type = seat.seat_type
        self.love_seats = seat.love_seats
        self.status = seat.status

    @classmethod
    def lock(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter(
            PlaySeat.pid == pid,
            PlaySeat.status == SeatStatus.ok.value,
            PlaySeat.sid.in_(sid_list)
        ).update({
            'orderno': orderno,
            'status': SeatStatus.locked.value,
            'lock_time': datetime.now()
        }, synchronize_session=False)
        if rows != len(sid_list):  # 如果rows的长度不等于sid的长度， 则执行回滚操作
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def unlock(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.locked.value
        ).update({
            'orderno': None,
            'status': SeatStatus.ok.value,
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def buy(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.locked.value
        ).update({
            'status': SeatStatus.sold.value,
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def refund(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.sold.value
        ).update({
            'status': SeatStatus.ok.value,
            'orderno': None
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def print_tickets(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno,
            status=SeatStatus.sold.value
        ).update({
            'status': SeatStatus.printed.value,
        }, synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def getby_orderno(cls, orderno):
        return cls.query.filter_by(orderno=orderno).all()