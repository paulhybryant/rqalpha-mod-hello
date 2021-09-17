# -*- coding: utf-8 -*-
import pandas as pd
from rqalpha.api import *
from rqalpha import run
import pathlib

def init(context):
    logger.info("init")
    #  context.s1 = "000001.XSHE"
    context.s1 = "128022.XSHE"
    #  update_universe(context.s1)
    context.fired = False

def before_trading(context):
    pass

def handle_bar(context, bar_dict):
    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order = order_percent(context.s1, 1)
        logger.info(order)
        context.fired = True

config = {
    "base": {
        "start_date": "2018-07-17",
        "end_date": "2018-08-18",
        "accounts": {"stock": 100000},
        "frequency": "1d",
        "benchmark": None,
        "strategy_file": __file__
    },
    "extra": {
        "log_level": "verbose",
    },
    "mod": {
        "sys_analyser": {
            "enabled": True,
            # "report_save_path": ".",
            #  "plot": True
        },
        "sys_simulation": {
            "enabled": True,
            # "matching_type": "last"
        },
        "local_source": {
            "enabled": True,
            "lib": "rqalpha_mod_local_source",
            # 其他配置参数
            "start_date": "2018-01-01",
            "end_date": "2021-09-08",
            "data_path": pathlib.Path(__file__).parent.joinpath("testdata.xlsx"),
        }
    }
}

if __name__ == "__main__":
    # 您可以指定您要传递的参数
    run(config=config)

