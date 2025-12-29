"""Module for computing technical indicators"""

import pandas as pd
import numpy as np
import ta
from typing import Dict, Tuple

class TechnicalIndicators:
    def __init__(self):
        pass

    def compute_indicators(self, df: pd.DataFrame, sma_period: int,
                          ema_fast: int, ema_slow: int, rsi_period: int,
                          macd_fast: int, macd_slow: int, macd_signal: int,
                          atr_period: int) -> Dict:
        """
        Compute all technical indicators for a timeframe
        Returns a dictionary of indicator values for each timeframe
        """
        # Basic price indicators
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3

        # SMA
        df['sma'] = ta.sma_indicator(df['close'], period=sma_period)

        # EMA
        df['ema_fast'] = ta.ema_indicator(df['close'], period=ema_fast)
        df['ema_slow'] = ta.ema_indicator(df['close'], period=ema_slow)

        # RSI
        df['rsi'] = ta.momentum.rsi(df['close'], timeperiod=rsi_period)

        # MACD
        df['macd'], df['signal'], df['macd_hist'] = ta.momentum.macd(
            df['close'], fastperiod=macd_fast, slowperiod=macd_slow, signalperiod=macd_signal)

        # ATR
        df['tr'] = ta.volatility.typical_true_range(df)
        df['atr'] = ta.volatility.atr(df['tr'], timeperiod=atr_period)

        # VWAP (for this timeframe)
        if len(df) > 0:
            df['vwap'] = df['typical_price'].cumsum() / df['volume'].cumsum()

        # Swing highs/lows (for level detection)
        df['swing_highs'] = self._find_swing_highs(df)
        df['swing_lows'] = self._find_swing_lows(df)

        # Return indicator values for each timeframe
        return {
            'close': df['close'].values,
            'open': df['open'].values,
            'high': df['high'].values,
            'low': df['low'].values,
            'volume': df['volume'].values,
            'sma': df['sma'].values,
            'ema_fast': df['ema_fast'].values,
            'ema_slow': df['ema_slow'].values,
            'rsi': df['rsi'].values,
            'macd': df['macd'].values,
            'signal': df['signal'].values,
            'macd_hist': df['macd_hist'].values,
            'atr': df['atr'].values,
            'vwap': df['vwap'].values,
            'swing_highs': df['swing_highs'].values,
            'swing_lows': df['swing_lows'].values,
            'typical_price': df['typical_price'].values
        }

    def _find_swing_highs(self, df: pd.DataFrame) -> np.ndarray:
        """Find swing highs using simple moving average crossover"""
        # Calculate 5-period moving average
        df['ma5'] = ta.sma_indicator(df['high'], period=5)

        # Find points where price crosses above MA5
        mask = (df['high'] > df['ma5']) & (df['high'] > df['high'].shift(1))
        return df.loc[mask, 'high'].values

    def _find_swing_lows(self, df: pd.DataFrame) -> np.ndarray:
        """Find swing lows using simple moving average crossover"""
        # Calculate 5-period moving average
        df['ma5'] = ta.sma_indicator(df['low'], period=5)

        # Find points where price crosses below MA5
        mask = (df['low'] < df['ma5']) & (df['low'] < df['low'].shift(1))
        return df.loc[mask, 'low'].values