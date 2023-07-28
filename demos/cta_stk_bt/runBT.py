from wtpy import WtBtEngine,EngineType
from Strategies.DualThrust import StraDualThrustStk
from wtpy.apps import WtBtAnalyst

if __name__ == "__main__":
    #创建一个运行环境，并加入策略
    engine = WtBtEngine(EngineType.ET_CTA)
    engine.init(folder='../common/', cfgfile="configbt.yaml", commfile="stk_comms.json", contractfile="stocks.json")
    engine.configBacktest(202104220930,202304281500)
    engine.configBTStorage(mode="csv", path="../storage/")
    engine.commitBTConfig()
    
    straInfo = StraDualThrustStk(name='pydt_SH510880', code="SSE.ETF.510880", barCnt=50, period="m5", days=30, k1=0.1, k2=0.1)
    engine.set_cta_strategy(straInfo)

    engine.run_backtest()

    #绩效分析
    analyst = WtBtAnalyst()
    analyst.add_strategy("pydt_SH510880", folder="./outputs_bt/", init_capital=10000, rf=0.0, annual_trading_days=240)
    analyst.run_flat()

    kw = input('press any key to exit\n')
    engine.release_backtest()