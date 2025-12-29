"""Module for calculating key price levels and support/resistance"""

import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
from .indicators import TechnicalIndicators

class PriceLevels:
    def __init__(self):
        self.indicators = TechnicalIndicators()

    def calculate_levels(self, df: pd.DataFrame, sma_period: int = 20) -> Dict:
        """
        Calculate key price levels including:
        - Support/Resistance
        - Fibonacci retracement
        - Volume weighted levels
        - Swing highs/lows
        """
        # Calculate basic indicators
        indicators = self.indicators.compute_indicators(df, sma_period, 12, 26, 14, 12, 26, 14, 14, 14)

        # Calculate support/resistance levels
        levels = self._calculate_support_resistance(df, indicators['sma'])

        # Calculate Fibonacci retracement levels
        fib_levels = self._calculate_fibonacci_levels(df)

        # Calculate volume-weighted levels
        volume_levels = self._calculate_volume_weighted_levels(df)

        # Combine all levels
        combined_levels = self._combine_levels(df, levels, fib_levels, volume_levels)

        return combined_levels

    def _calculate_support_resistance(self, df: pd.DataFrame, sma: np.ndarray) -> List[Tuple[float, str]]:
        """Calculate support/resistance levels using moving average and swing points"""
        levels = []

        # Find swing highs and lows
        swing_highs = self.indicators._find_swing_highs(df)
        swing_lows = self.indicators._find_swing_lows(df)

        # Add swing highs as resistance
        for high in swing_highs:
            levels.append((high, 'resistance'))

        # Add swing lows as support
        for low in swing_lows:
            levels.append((low, 'support'))

        # Add SMA as dynamic level
        levels.append((sma[-1], 'dynamic'))

        # Sort levels by price
        levels.sort()
        return levels

    def _calculate_fibonacci_levels(self, df: pd.DataFrame) -> List[Tuple[float, str]]:
        """Calculate Fibonacci retracement levels"""
        fib_levels = []
        
        # Find recent high and low
        high_idx = df['high'].idxmax()
        low_idx = df['low'].idxmin()
        
        # Calculate Fibonacci levels
        high_low_diff = df['high'].iloc[high_idx] - df['low'].iloc[low_idx]
        
        # 38.2%, 50%, 61.8% levels
        fib_levels.append((df['low'].iloc[low_idx] + 0.382 * high_low_diff, 'fib_38.2'))
        fib_levels.append((df['low'].iloc[low_idx] + 0.5 * high_low_diff, 'fib_50'))
        fib_levels.append((df['low'].iloc[low_idx] + 0.618 * high_low_diff, 'fib_61.8'))
        
        # Add to swing highs as resistance
        for level in fib_levels:
            fib_levels.append((level[0], 'resistance'))
        
        return fib_levels

    def _calculate_volume_weighted_levels(self, df: pd.DataFrame) -> List[Tuple[float, str]]:
        """Calculate volume-weighted levels"""
        volume_levels = []
        
        # Calculate cumulative volume weighted average
        df['vwap'] = df['typical_price'].cumsum() / df['volume'].cumsum()
        
        # Find local maxima/minima
        for i in range(1, len(df) - 1):
            if (df['vwap'].iloc[i] > df['vwap'].iloc[i-1] and df['vwap'].iloc[i] > df['vwap'].iloc[i+1]) or \
                (df['vwap'].iloc[i] < df['vwap'].iloc[i-1] and df['vwap'].iloc[i] < df['vwap'].iloc[i+1]):
                
                # Add to levels
                if df['vwap'].iloc[i] > df['vwap'].iloc[i-1]:
                    volume_levels.append((df['vwap'].iloc[i], 'volume_resistance'))
                else:
                    volume_levels.append((df['vwap'].iloc[i], 'volume_support'))

        return volume_levels

    def _combine_levels(self, df: pd.DataFrame, levels: List[Tuple[float, str]], 
                       fib_levels: List[Tuple[float, str]], volume_levels: List[Tuple[float, str]]) -> Dict:
        """Combine all levels into a single dictionary"""
        all_levels = []
        
        # Add all levels
        all_levels.extend(levels)
        all_levels.extend(fib_levels)
        all_levels.extend(volume_levels)
        
        # Remove duplicates
        unique_levels = []
        seen = set()
        for level in all_levels:
            if level not in seen:
                seen.add(level)
                unique_levels.append(level)
        
        # Sort by price
        unique_levels.sort()
        
        # Create result dictionary
        result = {}
        for price, level_type in unique_levels:
            result[price] = level_type
        
        return result