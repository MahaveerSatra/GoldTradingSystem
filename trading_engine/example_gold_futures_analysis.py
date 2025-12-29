import pandas as pd
from datetime import datetime, timedelta
from src.trading_engine.setup import TradingEngineSetup

def load_futures_data(filepath: str) -> pd.DataFrame:
    """Load and preprocess futures data from CSV file"""
    # Load data
    df = pd.read_csv(filepath)

    # Convert datetime column if needed
    if 'open_time' in df.columns:
        print("Would you like to convert 'open_time' to datetime format? (y/n): ", end="")
        convert_datetime = input().strip().lower()
        if convert_datetime == 'y':
            df['open_time'] = pd.to_datetime(df['open_time'])

    # Ensure proper datetime index
    if 'open_time' in df.columns:
        print("Would you like to set 'open_time' as the index? (y/n): ", end="")
        set_index = input().strip().lower()
        if set_index == 'y':
            df.set_index('open_time', inplace=True)

    # Filter for relevant time period
    print("Would you like to filter data by a custom time range? (y/n): ", end="")
    custom_range = input().strip().lower()
    if custom_range == 'y':
        print("Enter the start date (YYYY-MM-DD): ", end="")
        start_date_str = input()
        print("Enter the end date (YYYY-MM-DD): ", end="")
        end_date_str = input()
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            df = df[pd.to_datetime(df.index) >= (start_date)]
            df = df[pd.to_datetime(df.index) <= (end_date)]
        except ValueError:
            print("Invalid date format. Using default 30 days from now.")
            df = df[df.index >= datetime.now() - timedelta(days=30)]
    else:
        today = datetime.now()
        one_month_ago = today - timedelta(days=30)
        df = df[pd.to_datetime(df.index) >= one_month_ago]

    return df

def analyze_futures_data(df: pd.DataFrame) -> None:
    """Analyze futures data using the trading engine"""
    # Initialize trading engine
    setup = TradingEngineSetup()

    # Define session bounds (last 30 days by default)
    print("Would you like to use the default 30-day session? (y/n): ", end="")
    use_default = input().strip().lower()
    if use_default == 'n':
        print("Enter the start date (YYYY-MM-DD): ", end="")
        start_date_str = input()
        print("Enter the end date (YYYY-MM-DD): ", end="")
        end_date_str = input()
        try:
            session_start = datetime.strptime(start_date_str, "%Y-%m-%d")
            session_end = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using current date.")
            session_start = datetime.now()
            session_end = datetime.now()
    else:
        session_start = datetime.now() - timedelta(days=30)
        session_end = datetime.now()

    # Get session data
    print("How many rows would you like to analyze? (default: 10): ", end="")
    rows_input = input().strip()
    rows = int(rows_input) if rows_input else 10

    print("What value area percentage would you like to use? (default: 0.7): ", end="")
    value_area_input = input().strip()
    value_area = float(value_area_input) if value_area_input else 0.7

    session_data = setup.initialize_session(
        df=df,
        session_bounds=(session_start, session_end),
        rows=rows,
        value_area=value_area
    )

    # Print analysis results
    print("\n=== Futures Data Analysis Results ===")

    # Technical indicators
    print("\n1. Technical Indicators:")
    for indicator in session_data['indicators'].keys():
        print(f"   {indicator}: {session_data['indicators'][indicator]}")

    # Volume profile
    print("\n2. Volume Profile:")
    for profile in session_data['volume_profile']['time_intervals']:
        print(f"   Time: {profile[0].strftime('%Y-%m-%d %H:%M')} to {profile[1].strftime('%Y-%m-%d %H:%M')}")

    # Price levels
    print("\n3. Price Levels:")
    for price, level_type in session_data['price_levels'].items():
        print(f"   {price:.2f} - {level_type}")

    # Market bias
    print("\n4. Market Bias:")
    print(f"   Overall Bias: {session_data['bias']}")

    # Volume distribution
    print("\n5. Volume Distribution:")
    for interval, volume in session_data['volume_profile']['volume_distribution'].items():
        print(f"   {interval}: {volume}")

def main():
    """Main execution function"""
    # Example data file path - replace with your actual data file
    data_file = "micro_gold_futures.csv"

    print("Please enter the path to your data file:")
    data_file = input()

    try:
        # Load and analyze data
        df = load_futures_data(data_file)
        analyze_futures_data(df)

    except FileNotFoundError:
        print(f"Error: Data file '{data_file}' not found. Please ensure it exists in the working directory.")
    except Exception as e:
        print(f"An error occurred during analysis: {str(e)}")

if __name__ == "__main__":
    main()