from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title='Andrew K. Rockson Equity Research API', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

BASE_FCF = 66987.0
NET_CASH = 51414.0
SHARES = 7450.0
MARKET_PRICE = 481.63

class DCFRequest(BaseModel):
    growth_rates: List[float] = Field(default=[0.15,0.13,0.11,0.09,0.07], min_length=5, max_length=5)
    wacc: float = 0.085
    terminal_growth: float = 0.03
    base_fcf: float = BASE_FCF
    net_cash: float = NET_CASH
    shares: float = SHARES
    market_price: float = MARKET_PRICE

@app.get('/api/health')
def health(): return {'status':'ok'}

@app.get('/api/company/MSFT')
def company():
    return {'ticker':'MSFT','company':'Microsoft Corporation','market_price':MARKET_PRICE,'base_fcf':BASE_FCF,'net_cash':NET_CASH,'shares':SHARES}

@app.post('/api/dcf')
def dcf(req: DCFRequest):
    if req.wacc <= req.terminal_growth:
        raise HTTPException(400, 'WACC must be greater than terminal growth.')
    if req.shares <= 0:
        raise HTTPException(400, 'Shares must be greater than zero.')
    fcf = req.base_fcf
    pv_fcfs, forecasts = 0.0, []
    for year, g in enumerate(req.growth_rates, 1):
        fcf *= 1 + g
        pv = fcf / ((1 + req.wacc) ** year)
        pv_fcfs += pv
        forecasts.append({'year': 2026 + year, 'growth': g, 'fcf': round(fcf,2), 'pv': round(pv,2)})
    terminal_value = fcf * (1 + req.terminal_growth) / (req.wacc - req.terminal_growth)
    pv_terminal = terminal_value / ((1 + req.wacc) ** 5)
    enterprise_value = pv_fcfs + pv_terminal
    equity_value = enterprise_value + req.net_cash
    fair_value = equity_value / req.shares
    upside = fair_value / req.market_price - 1
    recommendation = 'UNDERVALUED' if upside >= .10 else ('FAIRLY VALUED' if upside > -.10 else 'OVERVALUED')
    return {'fair_value':round(fair_value,2),'market_price':req.market_price,'upside_downside':round(upside,4),'recommendation':recommendation,'enterprise_value':round(enterprise_value,2),'equity_value':round(equity_value,2),'terminal_value':round(terminal_value,2),'pv_terminal':round(pv_terminal,2),'forecast':forecasts}
