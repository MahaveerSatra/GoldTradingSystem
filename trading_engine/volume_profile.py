"""Volume Profile Module for analyzing volume distribution"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime

class VolumeProfile:
    def __init__(self):
        pass

    def compute_volume_profile(self, df: pd.DataFrame, session_bounds: Tuple[datetime, datetime], 
                             rows: int = 10, value_area: float = 0.7) -> Dict:
        """
        Compute volume profile for a given session
        Returns a dictionary with volume distribution
        """
        # Convert datetime to timestamp for easier slicing
        start_time = session_bounds[0].timestamp()
        end_time = session_bounds[1].timestamp()
        
        # Filter data within session bounds
        session_df = df[(df.index >= start_time) & (df.index <= end_time)].copy()
        
        # Calculate time intervals
        time_intervals = self._calculate_time_intervals(session_df, rows)
        
        # Calculate volume distribution
        volume_distribution = self._calculate_volume_distribution(session_df, time_intervals)
        
        # Calculate value area percentage
        value_area_percent = self._calculate_value_area_percent(session_df, time_intervals, value_area)
        
        # Calculate volume profile
        volume_profile = self._calculate_volume_profile(session_df, time_intervals, value_area_percent)
        
        return {
            'time_intervals': time_intervals,
            'volume_distribution': volume_distribution,
            'value_area_percent': value_area_percent,
            'volume_profile': volume_profile
        }

    def _calculate_time_intervals(self, df: pd.DataFrame, rows: int = 10) -> List[Tuple[datetime, datetime]]:
        """Calculate evenly spaced time intervals"""
        time_intervals = []
        
        # Get session start and end
        start_time = df.index[0]
        end_time = df.index[-1]
        
        # Calculate interval duration
        duration = (end_time - start_time) / rows
        
        # Create time intervals
        for i in range(rows):
            interval_start = start_time + i * duration
            interval_end = interval_start + duration
            time_intervals.append((interval_start, interval_end))
        
        return time_intervals

    def _calculate_volume_distribution(self, df: pd.DataFrame, time_intervals: List[Tuple[datetime, datetime]]) -> Dict:
        """Calculate volume distribution across time intervals"""
        volume_distribution = {}
        
        for i, (start, end) in enumerate(time_intervals):
            # Filter data for current interval
            interval_df = df[(df.index >= start) & (df.index <= end)]
            
            # Calculate volume
            volume = interval_df['volume'].sum()
            
            # Store volume distribution
            volume_distribution[f'time_interval_{i}'] = volume
        
        return volume_distribution

    def _calculate_value_area_percent(self, df: pd.DataFrame, time_intervals: List[Tuple[datetime, datetime]], 
                                    value_area: float = 0.7) -> float:
        """Calculate value area percentage"""
        # Calculate total volume
        total_volume = df['volume'].sum()
        
        # Calculate value area
        value_area_volume = self._calculate_value_area(df)
        
        # Calculate value area percentage
        value_area_percent = (value_area_volume / total_volume) * 100
        
        return value_area_percent

    def _calculate_value_area(self, df: pd.DataFrame) -> float:
        """Calculate value area for a DataFrame"""
        # Calculate cumulative volume
        cum_volume = df['volume'].cumsum()
        
        # Calculate value area
        value_area = (df['close'] * cum_volume).sum()
        
        return value_area

    def _calculate_volume_profile(self, df: pd.DataFrame, time_intervals: List[Tuple[datetime, datetime]], 
                                value_area_percent: float) -> Dict:
        """Calculate volume profile with value area consideration"""
        # Calculate volume distribution
        volume_distribution = self._calculate_volume_distribution(df, time_intervals)
        
        # Calculate volume profile
        volume_profile = {}
        
        # Sort time intervals by volume
        sorted_intervals = sorted(
            [(vol, idx) for idx, vol in volume_distribution.items()],
            reverse=True
        )
        
        # Create profile with volume and percentage
        for i, (vol, idx) in enumerate(sorted_intervals):
            # Calculate percentage of total volume
            profile_vol = vol / sum(volume_distribution.values())
            
            # Store volume profile
            volume_profile[f'profile_{i}'] = {
                'volume': vol,
                'percentage': profile_vol * 100,
                'time_interval': idx
            }
        
        # Add value area information
        value_area_info = {
            'total_value_area': self._calculate_value_area(df),
            'percentage_of_value_area': value_area_percent
        }
        
        volume_profile['value_area_info'] = value_area_info
        
        return volume_profile