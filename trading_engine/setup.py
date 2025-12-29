"""Trading Engine Setup Module"""

from typing import Dict, Tuple
from datetime import datetime
import pandas as pd
from .indicators import TechnicalIndicators
from .volume_profile import VolumeProfile
from .levels import PriceLevels
from .bias import MarketBias
from .stop_loss import StopLossManager

class TradingEngineSetup:
    def __init__(self):
        self.indicators = TechnicalIndicators()
        self.volume_profile = VolumeProfile()
        self.price_levels = PriceLevels()
        self.bias_detector = MarketBias()
        self.stop_loss = StopLossManager()

    def initialize_session(self, df: pd.DataFrame, session_bounds: Tuple[datetime, datetime], 
                          rows: int = 10, value_area: float = 0.7) -> Dict:
        """
        Initialize and prepare trading session data
        Returns a dictionary with all prepared data
        """
        # Calculate technical indicators
        indicators = self.indicators.compute_indicators(
            df, sma_period=20, ema_fast=12, ema_slow=26, rsi_period=14,
            macd_fast=12, macd_slow=26, macd_signal=14, atr_period=14
        )

        # Calculate volume profile
        volume_profile = self.volume_profile.compute_volume_profile(
            df, session_bounds, rows, value_area
        )

        # Calculate price levels
        price_levels = self.price_levels.calculate_levels(df)

        # Detect market bias
        bias = self.bias_detector.detect_bias(df)

        return {
            'indicators': indicators,
            'volume_profile': volume_profile,
            'price_levels': price_levels,
            'bias': bias
        }

    def prepare_trading_strategy(self, df: pd.DataFrame, sma_period: int = 20) -> Dict:
        """
        Prepare trading strategy data by calculating all necessary components
        """
        # Calculate technical indicators
        indicators = self.indicators.compute_indicators(df, sma_period=sma_period)

        # Calculate price levels
        price_levels = self.price_levels.calculate_levels(df, sma_period=sma_period)

        # Detect market bias
        bias = self.bias_detector.detect_bias(df, sma_period=sma_period)

        return {
            'indicators': indicators,
            'price_levels': price_levels,
            'bias': bias
        }