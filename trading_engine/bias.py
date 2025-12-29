"""Module for detecting market bias and trend direction"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from .indicators import TechnicalIndicators

class MarketBias:
    def __init__(self):
        self.indicators = TechnicalIndicators()

    def detect_bias(self, df: pd.DataFrame, sma_period: int = 20) -> Dict:
        """
        Detect market bias using multiple indicators:
        - Moving average crossovers
        - MACD histogram
        - RSI overbought/oversold
        - Volume trend
        """
        # Calculate indicators
        indicators = self.indicators.compute_indicators(df, sma_period, 12, 26, 14, 12, 26, 14, 14, 14)

        # Detect trend bias
        trend_bias = self._detect_trend_bias(df, indicators['sma'], indicators['ema_fast'], indicators['ema_slow'])

        # Detect momentum bias
        momentum_bias = self._detect_momentum_bias(df, indicators['macd'], indicators['signal'], indicators['rsi'])

        # Detect volume bias
        volume_bias = self._detect_volume_bias(df)

        # Combine all biases
        return {
            'trend_bias': trend_bias,
            'momentum_bias': momentum_bias,
            'volume_bias': volume_bias,
            'overall_bias': self._combine_bias(trend_bias, momentum_bias, volume_bias)
        }

    def _detect_trend_bias(self, df: pd.DataFrame, sma: np.ndarray, ema_fast: np.ndarray, ema_slow: np.ndarray) -> str:
        """Detect trend bias using moving averages"""
        # Check SMA crossover
        sma_crossover = self._check_sma_crossover(df, sma)
        
        # Check EMA crossover
        ema_crossover = self._check_ema_crossover(df, ema_fast, ema_slow)
        
        # Determine trend bias
        if sma_crossover == 'bullish' and ema_crossover == 'bullish':
            return 'bullish_trend'
        elif sma_crossover == 'bearish' and ema_crossover == 'bearish':
            return 'bearish_trend'
        elif sma_crossover == 'bullish' and ema_crossover == 'bearish':
            return 'overbought_trend'
        elif sma_crossover == 'bearish' and ema_crossover == 'bullish':
            return 'oversold_trend'
        else:
            return 'neutral_trend'

    def _check_sma_crossover(self, df: pd.DataFrame, sma: np.ndarray) -> str:
        """Check if SMA is crossing above/below price"""
        # Find crossover points
        crossovers = []
        for i in range(1, len(df)):
            if df['close'].iloc[i] > sma.iloc[i-1] and df['close'].iloc[i-1] <= sma.iloc[i-1]:
                crossovers.append('bullish')
            elif df['close'].iloc[i] < sma.iloc[i-1] and df['close'].iloc[i-1] >= sma.iloc[i-1]:
                crossovers.append('bearish')

        # Determine overall bias
        if len(crossovers) > 0:
            return crossovers[-1]  # Last crossover determines bias
        return 'neutral'

    def _check_ema_crossover(self, df: pd.DataFrame, ema_fast: np.ndarray, ema_slow: np.ndarray) -> str:
        """Check if EMAs are crossing above/below price"""
        # Find crossover points
        crossovers = []
        for i in range(1, len(df)):
            if ema_fast.iloc[i] > ema_slow.iloc[i-1] and ema_fast.iloc[i-1] <= ema_slow.iloc[i-1]:
                crossovers.append('bullish')
            elif ema_fast.iloc[i] < ema_slow.iloc[i-1] and ema_fast.iloc[i-1] >= ema_slow.iloc[i-1]:
                crossovers.append('bearish')

        # Determine overall bias
        if len(crossovers) > 0:
            return crossovers[-1]  # Last crossover determines bias
        return 'neutral'

    def _detect_momentum_bias(self, df: pd.DataFrame, macd: np.ndarray, signal: np.ndarray, rsi: np.ndarray) -> str:
        """Detect momentum bias using MACD and RSI"""
        # Check MACD histogram
        macd_hist = macd - signal
        
        # Check RSI overbought/oversold
        rsi_bias = 'oversold' if rsi.mean() < 30 else 'overbought' if rsi.mean() > 70 else 'neutral'

        # Determine overall bias
        if macd_hist.mean() > 0 and rsi_bias == 'oversold':
            return 'bullish_momentum'
        elif macd_hist.mean() < 0 and rsi_bias == 'overbought':
            return 'bearish_momentum'
        else:
            return 'neutral_momentum'

    def _detect_volume_bias(self, df: pd.DataFrame) -> str:
        """Detect volume bias using volume trend"""
        # Calculate volume trend
        volume_trend = df['volume'].diff().mean()
        
        # Determine bias
        if volume_trend > 0:
            return 'bullish_volume'
        elif volume_trend < 0:
            return 'bearish_volume'
        else:
            return 'neutral_volume'

    def _combine_bias(self, trend: str, momentum: str, volume: str) -> str:
        """Combine all biases into a single overall bias"""
        # Weighted combination of biases
        if trend == 'bullish_trend' and momentum == 'bullish_momentum' and volume == 'bullish_volume':
            return 'strong_bullish'
        elif trend == 'bearish_trend' and momentum == 'bearish_momentum' and volume == 'bearish_volume':
            return 'strong_bearish'
        elif trend == 'bullish_trend' and momentum == 'bullish_momentum':
            return 'moderate_bullish'
        elif trend == 'bearish_trend' and momentum == 'bearish_momentum':
            return 'moderate_bearish'
        elif trend == 'bullish_trend':
            return 'weak_bullish'
        elif trend == 'bearish_trend':
            return 'weak_bearish'
        elif momentum == 'bullish_momentum':
            return 'momentum_bullish'
        elif momentum == 'bearish_momentum':
            return 'momentum_bearish'
        else:
            return 'neutral_bias'