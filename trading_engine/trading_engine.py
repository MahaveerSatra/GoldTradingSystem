"""Core Trading Engine Module"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .setup import TradingEngineSetup
from .stop_loss import StopLossManager

class TradingEngine:
    def __init__(self):
        self.setup = TradingEngineSetup()
        self.stop_loss = StopLossManager()

    def analyze_session(self, df: pd.DataFrame, session_bounds: Tuple[datetime, datetime], 
                       rows: int = 10, value_area: float = 0.7) -> Dict:
        """
        Analyze a trading session and return comprehensive trading signals
        """
        # Initialize session data
        session_data = self.setup.initialize_session(df, session_bounds, rows, value_area)

        # Generate trading signals
        signals = self._generate_signals(df, session_data)

        # Calculate risk management parameters
        risk_params = self._calculate_risk_parameters(df, session_data)

        return {
            'session_data': session_data,
            'trading_signals': signals,
            'risk_parameters': risk_params
        }

    def analyze_strategy(self, df: pd.DataFrame, sma_period: int = 20) -> Dict:
        """
        Analyze a trading strategy and return entry/exit points
        """
        # Prepare strategy data
        strategy_data = self.setup.prepare_trading_strategy(df, sma_period)

        # Generate trading signals
        signals = self._generate_signals(df, strategy_data)

        # Calculate risk management parameters
        risk_params = self._calculate_risk_parameters(df, strategy_data)

        return {
            'strategy_data': strategy_data,
            'trading_signals': signals,
            'risk_parameters': risk_params
        }

    def _generate_signals(self, df: pd.DataFrame, data: Dict) -> Dict:
        """
        Generate trading signals based on session/strategy data
        """
        signals = {
            'entries': [],
            'exits': [],
            'trades': []
        }

        # Get indicators from data
        indicators = data['indicators']
        price_levels = data['price_levels']
        bias = data['bias']

        # Entry signals
        if bias['overall_bias'] == 'strong_bullish':
            signals['entries'].append({
                'type': 'bullish_entry',
                'price': df['close'].iloc[-1],
                'time': df.index[-1]
            })
        elif bias['overall_bias'] == 'strong_bearish':
            signals['entries'].append({
                'type': 'bearish_entry',
                'price': df['close'].iloc[-1],
                'time': df.index[-1]
            })

        # Exit signals based on price levels
        for price, level_type in price_levels.items():
            if level_type == 'resistance':
                signals['exits'].append({
                    'type': 'resistance_exit',
                    'price': price,
                    'time': df[df['close'] >= price].index[-1]
                })
            elif level_type == 'support':
                signals['exits'].append({
                    'type': 'support_exit',
                    'price': price,
                    'time': df[df['close'] <= price].index[-1]
                })

        # Combine entries and exits
        for entry in signals['entries']:
            for exit in signals['exits']:
                signals['trades'].append({
                    'entry': entry,
                    'exit': exit,
                    'profit': exit['price'] - entry['price']
                })

        return signals

    def _calculate_risk_parameters(self, df: pd.DataFrame, data: Dict) -> Dict:
        """
        Calculate risk management parameters
        """
        # Get indicators
        indicators = data['indicators']
        price_levels = data['price_levels']
        
        # Calculate stop loss levels
        stop_loss = self.stop_loss.calculate_stop_loss(df, price_levels)

        # Calculate take profit levels
        take_profit = self.stop_loss.calculate_take_profit(df, price_levels)

        # Calculate risk/reward ratio
        risk_reward = self.stop_loss.calculate_risk_reward(df, price_levels)

        return {
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk_reward': risk_reward
        }

    def execute_trade(self, trade: Dict, df: pd.DataFrame) -> Dict:
        """
        Execute a trade based on signals and risk parameters
        """
        # Validate trade parameters
        if not self._validate_trade(trade):
            return {'status': 'invalid', 'message': 'Trade parameters invalid'}

        # Calculate position size
        position_size = self._calculate_position_size(trade, df)

        # Execute trade
        trade_result = {
            'status': 'executed',
            'entry': trade['entry'],
            'exit': trade['exit'],
            'profit': trade['exit']['price'] - trade['entry']['price'],
            'position_size': position_size,
            'risk_reward': trade['risk_reward']
        }

        return trade_result

    def _validate_trade(self, trade: Dict) -> bool:
        """Validate trade parameters"""
        # Check required fields
        required_fields = ['entry', 'exit', 'risk_reward']
        for field in required_fields:
            if field not in trade:
                return False

        # Check price difference
        if abs(trade['exit']['price'] - trade['entry']['price']) < 0.01:
            return False

        return True

    def _calculate_position_size(self, trade: Dict, df: pd.DataFrame) -> float:
        """Calculate position size based on risk parameters"""
        # Get risk parameters
        risk = trade['risk_reward']['risk']
        reward = trade['risk_reward']['reward']
        
        # Calculate position size
        position_size = abs(trade['exit']['price'] - trade['entry']['price']) * 0.01 / risk
        
        # Ensure position size is reasonable
        if position_size < 0.001:
            position_size = 0.001
        
        return position_size