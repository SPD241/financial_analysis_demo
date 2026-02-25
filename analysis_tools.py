import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class AnalysisTools:
    
    '''
    Docstring for AnalysisTools
    '''

    def __init__(self):
        pass

        '''This is nothing for initilize in a general context'''


    def Relative_Strength_Index(self, data, period = 14):

        '''
        Docstring for Relative_Strength_Index
        
        :param data: the data within *DataFrame
        :param period: it is a constant, it is P = 1/f, always will calculate the following items with a period of 14
        :return: this funciton returns a dataframe which will be processed by app.py 
        '''
        delta = data["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(alpha=1/period, adjust = False).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust = False).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return pd.DataFrame({
            "RS": rs,
            "RSI": rsi
        }, index= data.index)
    
    def macd (self, data, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:

        '''
        Docstring for macd
        
        :param data: the data within *DataFrame
        :param fast: it a constant value, as a window
        :type fast: int
        :param slow: it a constant value, as a window
        :type slow: int
        :param signal: it a constant value, as a window
        :type signal: int
        :return: will return a DataFrame
        :rtype: DataFrame
        '''

        close = data['Close'].astype(float)

        ema_fast = close.ewm(span = fast, adjust = False).mean()
        ema_slow = close.ewm(span = slow, adjust = False).mean()

        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span = signal, adjust = False).mean()
        hist = macd_line - signal_line

        out = pd.DataFrame({
            "MACD": macd_line,
            "Signal": signal_line,
            "Histogram": hist
        }, index=data.index)

        return out
    
    def bollinger_bands(self, data, period: int = 20, k: float = 2.0) -> pd.DataFrame:
        '''
        Docstring for bollinger_bands
        
        :param data: the data within *DataFrame
        :param period: Description
        :type period: int
        :param k: constant for standard desviation
        :type k: float
        :return: will return a DataFrame
        :rtype: DataFrame
        '''

        close = data['Close'].astype(float)

        mb = close.rolling(period).mean()
        std = close.rolling(period).std()

        ub = mb + k * std
        lb = mb - k * std

        out = pd.DataFrame({
            "MB": mb,
            "UB": ub,
            "LB": lb
        }, index = data.index)

        return out
    
    def moving_average (self, data, window = (10, 20, 50), kind: str = "SMA") -> pd.DataFrame: 

        close = data["Close"].astype(float)

        out = pd.DataFrame(index=data.index)
        kind = kind.upper()

        for w in window: 
            if kind == "SMA":
                out[f"SMA_{w}"] = close.rolling(w).mean()
            elif kind == "EMA": 
                out[f"EMA_{w}"] = close.ewm(span=w, adjust = False).mean()
            else: 
                print("Error")

        return out
    
    def candlestick_patterns (self, data, doji_ratio: float = 0.1) -> pd.DataFrame:

        '''
        Docstring for candlestick_patterns
        
        :param data: the data within *DataFrame
        :param doji_ratio: Description
        :type doji_ratio: float
        :return: will return a DataFrame
        :rtype: DataFrame
        '''
        
        o = data["Open"].astype(float)
        h = data["High"].astype(float)
        l = data["Low"].astype(float)
        c = data["Close"].astype(float)

        body = (c - o).abs()
        rng = (h - 1).replace(0, np.nan)

        upper = h - np.maximum(o, c)
        lower = np.minimum(o, c) - 1

        doji = (body/rng) <= doji_ratio
        hammer = (lower >= 2 * body) & (upper <= 0.3 * body) & (body / rng <= 0.3)

        prev_o = o.shift(1)
        prev_c = c.shift(1)
        bullish_engulfing = (prev_c < prev_o) & (c > o) & (o < prev_c) & (c > prev_o)

        return pd.DataFrame({
            "Doji": doji.fillna(False),
            "Hammer": hammer.fillna(False),
            "Bullish_Engulfing": bullish_engulfing.fillna(False)
        }, index=data.index)
    
    def ichimoku_cloud (self, data, tenkan: int = 9, kijun: int = 26, senkou: int = 52, shift: int = 26) -> pd.DataFrame:

        '''
        Docstring for ichimoku_cloud
        
        :param data: the data within *DataFrame
        :param tenkan: Description
        :type tenkan: int
        :param kijun: Description
        :type kijun: int
        :param senkou: Description
        :type senkou: int
        :param shift: Description
        :type shift: int
        :return: will return a DataFrame
        :rtype: DataFrame
        '''

        h = data["High"].astype(float)
        l = data["Low"].astype(float)
        c = data["Close"].astype(float)

        tenkan_sen = (h.rolling(tenkan).max() + l.rolling(tenkan).min()) / 2
        kijun_sen = (h.rolling(kijun).max() + l.rolling(kijun).min()) / 2

        span_a = ((tenkan_sen + kijun_sen) / 2).shift(shift)
        span_b = ((h.rolling(senkou).max() + l.rolling(senkou).min()) / 2).shift(shift)

        chikou = c.shift(-shift)

        return pd.DataFrame({
            "Tenkan": tenkan_sen,
            "Kijun": kijun_sen,
            "Span_A": span_a,
            "Span_B": span_b,
            "Chikou": chikou
        },index=data.index)