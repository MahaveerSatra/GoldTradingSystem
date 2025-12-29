"""Module for calculating and managing stop loss and take profit levels"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List

class StopLossManager:
    def __init__(self):
        pass

    def calculate_stop_loss(self, df: pd.DataFrame, price_levels: Dict[float, str]) -> Dict:
        """
        Calculate stop loss levels based on price levels and volatility
        """
        # Extract price levels
        levels = list(price_levels.keys())
        levels.sort()
        
        # Calculate volatility using ATR
        atr = self._calculate_atr(df, 14)
        
        # Calculate stop loss levels
        stop_loss = {}
        
        # Dynamic stop loss based on volatility
        for i, price in enumerate(levels):
            # Add 1 ATR to the lower price level
            stop_loss[price] = price - atr
            
            # Ensure stop loss is below the nearest support level
            if i > 0 and price_levels[levels[i-1]] == 'support':
                stop_loss[price] = min(stop_loss[price], levels[i-1] - atr)
        
        return stop_loss

    def calculate_take_profit(self, df: pd.DataFrame, price_levels: Dict[float, str]) -> Dict:
        """
        Calculate take profit levels based on price levels and volatility
        """
        # Extract price levels
        levels = list(price_levels.keys())
        levels.sort()
        
        # Calculate volatility using ATR
        atr = self._calculate_atr(df, 14)
        
        # Calculate take profit levels
        take_profit = {}
        
        # Dynamic take profit based on volatility and resistance levels
        for i, price in enumerate(levels):
            # Add 1 ATR to the upper price level
            take_profit[price] = price + atr
            
            # Ensure take profit is above the nearest resistance level
            if i < len(levels) - 1 and price_levels[levels[i+1]] == 'resistance':
                take_profit[price] = max(take_profit[price], levels[i+1] + atr)
        
        return take_profit

    def calculate_risk_reward(self, df: pd.DataFrame, price_levels: Dict[float, str]) -> Dict:
        """
        Calculate risk/reward ratio based on price levels
        """
        # Extract price levels
        levels = list(price_levels.keys())
        levels.sort()
        
        # Calculate risk (distance to stop loss)
        risk = 0
        for i, price in enumerate(levels):
            if price_levels[price] == 'support':
                risk = price - (price_levels[levels[i-1]] - atr)  # Ensure we don't go below previous support
                break
        
        # Calculate reward (distance to nearest resistance)
        reward = 0
        for i, price in enumerate(levels):
            if price_levels[price] == 'resistance':
                reward = levels[i+1] - price
                break
        
        # Calculate ATR for volatility
        atr = self._calculate_atr(df, 14)
        
        # Adjust risk/reward ratio based on volatility
        risk_reward_ratio = reward / risk
        
        # Ensure reasonable ratio
        if risk_reward_ratio < 1.0:
            risk_reward_ratio = 1.0
        
        return {
            'risk': risk,
            'reward': reward,
            'ratio': risk_reward_ratio
        }

    def _calculate_atr(self, df: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range (ATR) for volatility measurement"""
        try:
            # Calculate True Range
            tr = np.maximum(df['high'] - df['low'], 0)
            tr = np.maximum(tr, abs(df['high'] - df['close'].shift(1)))
            tr = np.maximum(tr, abs(df['low'] - df['close'].shift(1)))
            
            # Calculate ATR
            atr = np.mean(tr.rolling(window=period).sum())

            # Calculate ATR
            if period <= 0:
                raise ValueError("Period must be greater than 0")

            if len(tr) < period:
                raise ValueError(f"Insufficient data points for ATR calculation with period {period}")

            atr = np.mean(tr.rolling(window=period).sum())
            return atr
            
        except Exception as e:
            print(f"Error calculating ATR: {str(e)}")
        return atr