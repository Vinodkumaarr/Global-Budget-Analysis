from sqlalchemy import create_engine
import pandas as pd


def analyze_budget_volatility(country_name):
    engine = create_engine("mysql+pymysql://root:msvinod3827#@localhost/global_budget_db")

    # Extract historical spending sequence
    query = """
        SELECT b.year, b.total_budget_billions_usd
        FROM budgets b
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s
        ORDER BY b.year ASC;
    """

    df = pd.read_sql(query, engine, params=(country_name,))

    if df.empty:
        return

    # Calculate a 10-year rolling Mean and Standard Deviation using Pandas
    df['rolling_mean'] = df['total_budget_billions_usd'].rolling(window=10).mean()
    df['rolling_std'] = df['total_budget_billions_usd'].rolling(window=10).std()

    # Calculate Volatility Index (Coefficient of Variation)
    df['volatility_index'] = (df['rolling_std'] / df['rolling_mean']) * 100

    return df


def compute_sector_correlations(country_name):
    engine = create_engine("mysql+pymysql://root:1243@localhost/global_budget_db")

    # Query all sector percentages for a country over its entire history
    query = """
        SELECT b.year, sa.sector_name, sa.allocated_percentage
        FROM sector_allocations sa
        JOIN budgets b ON sa.budget_id = b.budget_id
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s;
    """

    df = pd.read_sql(query, engine, params=(country_name,))

    if df.empty:
        return

    # Pivot table from long form back to wide format to compute cross-correlation metrics
    wide_df = df.pivot(index='year', columns='sector_name', values='allocated_percentage')

    # Calculate the Pearson Correlation Matrix
    correlation_matrix = wide_df.corr()

    return correlation_matrix
