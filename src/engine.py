from datetime import timedelta
from datetime import datetime as dt
import numpy as np

def get_data_pair(data_map, data_name, side, start_date='', end_date='', per_expiration=False):
    data_pair = dict()
    exp_map_side = 'callExpDateMap' if side.lower() == 'c' else 'putExpDateMap'
    for date in data_map[exp_map_side]:
        if dt.strptime(date[:10], '%Y-%m-%d') >= dt.strptime(start_date, '%Y-%m-%d') and dt.strptime(date[:10], '%Y-%m-%d') <= dt.strptime(end_date, '%Y-%m-%d'):
            for strike in data_map[exp_map_side][date]:
                value = data_map[exp_map_side][date][strike][0][data_name]
                if per_expiration:
                    data_pair.setdefault(float(strike), []).append(value)
                else:
                    if float(strike) in data_pair:
                        data_pair[float(strike)] += value
                    else:
                        data_pair[float(strike)] = value
    return data_pair

def get_gamma_exposure(call_gamma, put_gamma, call_oi, put_oi, spot_price):
    def gex_by_strike(gamma_dict, oi_dict):
        result = {}
        for strike, gammas in gamma_dict.items():
            ois = oi_dict.get(strike, [0] * len(gammas))
            result[strike] = sum(g * o for g, o in zip(gammas, ois)) * 100 * spot_price**2 * 0.01 / 1_000_000
        return result

    call_gex = gex_by_strike(call_gamma, call_oi)
    put_gex = gex_by_strike(put_gamma, put_oi)

    all_strikes = set(call_gex) | set(put_gex)
    return {s: call_gex.get(s, 0) - put_gex.get(s, 0) for s in all_strikes}

def get_delta_exposure(call_delta, put_delta, call_oi, put_oi):
    def dex_by_strike(delta_dict, oi_dict):
        result = {}
        for strike, deltas in delta_dict.items():
            ois = oi_dict.get(strike, [0] * len(deltas))
            result[strike] = sum(d * o for d, o in zip(deltas, ois)) * 100 / 1_000_000
        return result

    call_dex = dex_by_strike(call_delta, call_oi)
    put_dex = dex_by_strike(put_delta, put_oi)

    all_strikes = set(call_dex) | set(put_dex)
    return {s: call_dex.get(s, 0) + put_dex.get(s, 0) for s in all_strikes}
