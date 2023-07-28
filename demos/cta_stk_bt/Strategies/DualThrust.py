# from wtpy import BaseCtaStrategy
# from wtpy import CtaContext
# import numpy as np

# class StraDualThrustStk(BaseCtaStrategy):
    
#     def __init__(self, name:str, code:str, barCnt:int, period:str, days:int, k1:float, k2:float):
#         BaseCtaStrategy.__init__(self, name)

#         self.__days__ = days
#         self.__k1__ = k1
#         self.__k2__ = k2

#         self.__period__ = period
#         self.__bar_cnt__ = barCnt
#         self.__code__ = code

#     def on_init(self, context:CtaContext):
#         code = self.__code__    #品种代码

#         context.stra_get_bars(code, self.__period__, self.__bar_cnt__, isMain = True)
#         context.stra_log_text("DualThrust inited")

    
#     def on_calculate(self, context:CtaContext):
#         code = self.__code__    #品种代码

#         #读取最近50条1分钟线(dataframe对象)
#         df_bars = context.stra_get_bars(code, self.__period__, self.__bar_cnt__, isMain = True)

#         #把策略参数读进来，作为临时变量，方便引用
#         days = self.__days__
#         k1 = self.__k1__
#         k2 = self.__k2__

#         #平仓价序列、最高价序列、最低价序列
#         closes = df_bars.closes
#         highs = df_bars.highs
#         lows = df_bars.lows

#         #读取days天之前到上一个交易日位置的数据
#         hh = np.amax(highs[-days:-1])
#         hc = np.amax(closes[-days:-1])
#         ll = np.amin(lows[-days:-1])
#         lc = np.amin(closes[-days:-1])

#         #读取今天的开盘价、最高价和最低价
#         # lastBar = df_bars.get_last_bar()
#         openpx = df_bars.opens[-1]
#         highpx = df_bars.highs[-1]
#         lowpx = df_bars.lows[-1]

#         '''
#         !!!!!这里是重点
#         1、首先根据最后一条K线的时间，计算当前的日期
#         2、根据当前的日期，对日线进行切片,并截取所需条数
#         3、最后在最终切片内计算所需数据
#         '''

#         #确定上轨和下轨
#         upper_bound = openpx + k1* max(hh-lc,hc-ll)
#         lower_bound = openpx - k2* max(hh-lc,hc-ll)

#         #读取当前仓位
#         curPos = context.stra_get_position(code)

#         if curPos == 0:
#             if highpx >= upper_bound:
#                 context.stra_enter_long(code, 1, 'enterlong')
#                 context.stra_log_text("向上突破%.2f<=%.2f，多仓进场" % (highpx, upper_bound))
#                 return
#         elif curPos > 0:
#             if lowpx <= lower_bound:
#                 context.stra_exit_long(code, curPos, 'exitlong')
#                 context.stra_log_text("向下突破%.2f<=%.2f，多仓出场" % (lowpx, lower_bound))
#                 return


#     def on_tick(self, context:CtaContext, stdCode:str, newTick:dict):
#         #context.stra_log_text ("on tick fired")
#         return


from wtpy import BaseCtaStrategy
from wtpy import CtaContext
import numpy as np

class StraDualThrustStk(BaseCtaStrategy):
    
    def __init__(self, name:str, code:str, barCnt:int, period:str, days:int, k1:float, k2:float):
        BaseCtaStrategy.__init__(self, name)

        self.__days__ = days
        self.__k1__ = k1
        self.__k2__ = k2

        self.__period__ = period
        self.__bar_cnt__ = barCnt
        self.__code__ = code

        self.last_trade_date = None
        self.count = 0
        self.pos = False

        self.period = 2



    def on_init(self, context:CtaContext):
        code = self.__code__    #品种代码
        

        context.stra_get_bars(code, self.__period__, self.__bar_cnt__, isMain = True)
        context.stra_get_bars('SSE.ETF.000001', self.__period__, self.__bar_cnt__, isMain = False)
        context.stra_log_text("DualThrust inited")

    
    def on_calculate(self, context:CtaContext):
        code = self.__code__    #品种代码

        cur_date = context.get_date()
        cur_time = context.get_time()

        if cur_date is None or cur_date != self.last_trade_date:
            if self.pos:
                self.count += 1
            self.last_trade_date = cur_date

        #读取最近50条1分钟线(dataframe对象)
        df_bars = context.stra_get_bars(code, self.__period__, 1, isMain = True)
        sh_bars = context.stra_get_bars('SSE.ETF.000001', self.__period__, 1, isMain = False)
        curPos = context.stra_get_position(code)
        
        if not self.pos:
            if cur_time == 935:  # 检查是否是第一个5分钟线
                # print(self.dataclose[0] ,self.dataclose[-1])
                if sh_bars.closes[-1] > sh_bars.opens[-1]:
                    context.stra_enter_long(code,3000)
                    context.stra_log_text(f"{cur_date} {cur_time} buy")
                    self.pos = True
                    self.count = 0
                    # cash = self.broker.get_cash()
                    # size = int(cash * 0.99 / self.data.close[0] / 100) * 100  # 计算最大可用资金买入的股数
                    # if size >= 100:
                    #     # print(f"create order size : {size}")
                    #     self.order = self.buy(size=max(size, 100))
                    #     # self.order = self.order_target_percent(target=0.98)
                    #     self.pos = True
                    #     self.count = 0
            return
        else:
            if self.count >= self.period and cur_time == 1455:  # 检查是否是收盘时间
                context.stra_exit_long(code, curPos, 'exitlong')
                context.stra_log_text(f"{cur_date} {cur_time} sell")
                self.pos = False
                self.count = 0
            return
        
        #把策略参数读进来，作为临时变量，方便引用
        # days = self.__days__
        # k1 = self.__k1__
        # k2 = self.__k2__

        # #平仓价序列、最高价序列、最低价序列
        # closes = df_bars.closes
        # highs = df_bars.highs
        # lows = df_bars.lows

        # #读取days天之前到上一个交易日位置的数据
        # hh = np.amax(highs[-days:-1])
        # hc = np.amax(closes[-days:-1])
        # ll = np.amin(lows[-days:-1])
        # lc = np.amin(closes[-days:-1])

        # #读取今天的开盘价、最高价和最低价
        # # lastBar = df_bars.get_last_bar()
        # openpx = df_bars.opens[-1]
        # highpx = df_bars.highs[-1]
        # lowpx = df_bars.lows[-1]

        # '''
        # !!!!!这里是重点
        # 1、首先根据最后一条K线的时间，计算当前的日期
        # 2、根据当前的日期，对日线进行切片,并截取所需条数
        # 3、最后在最终切片内计算所需数据
        # '''

        # #确定上轨和下轨
        # upper_bound = openpx + k1* max(hh-lc,hc-ll)
        # lower_bound = openpx - k2* max(hh-lc,hc-ll)

        # #读取当前仓位
        # curPos = context.stra_get_position(code)

        # if curPos == 0:
        #     if highpx >= upper_bound:
        #         context.stra_enter_long(code, 1, 'enterlong')
        #         context.stra_log_text("向上突破%.2f<=%.2f，多仓进场" % (highpx, upper_bound))
        #         return
        # elif curPos > 0:
        #     if lowpx <= lower_bound:
        #         context.stra_exit_long(code, curPos, 'exitlong')
        #         context.stra_log_text("向下突破%.2f<=%.2f，多仓出场" % (lowpx, lower_bound))
        #         return


    def on_tick(self, context:CtaContext, stdCode:str, newTick:dict):
        #context.stra_log_text ("on tick fired")
        return