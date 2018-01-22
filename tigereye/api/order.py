from datetime import datetime
from flask import request
from flask_classy import route
from tigereye.api import ApiView
from tigereye.extensions.validator import Validator, multi_int, mulit_comlex_int
from tigereye.helper.code import Code
from tigereye.models.movie import Movie
from tigereye.models.order import Order, OrderStatus
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat, SeatType


class OrderView(ApiView):

    @route('/refund/', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def refund(self):
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}

        refund_num = PlaySeat.refund(orderno, order.pid, seats) # 退票数量
        if not refund_num:
            return Code.ticket_refund_failed, {}
        order.status = OrderStatus.refund.value
        order.refund_time = datetime.now()
        order.save()
        return {'refund_num': refund_num}

    @route('/ticket/print/', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def print_ticket(self):
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']

        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}

        printed_num = PlaySeat.print_tickets(order.seller_order_no, order.pid, seats)

        if not printed_num:
            return Code.ticket_print_failed.value, {}
        order.status = OrderStatus.printed.value
        order.printed_time = datetime.now()
        order.save()
        return {'printed_num': printed_num}

    @route('/ticket/info/')
    @Validator(orderno=str)
    def ticket_info(self):
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        order.play = Play.get(order.pid)
        order.movie = Movie.get(order.play.mid)
        order.tickets = PlaySeat.getby_orderno(orderno)
        return order
