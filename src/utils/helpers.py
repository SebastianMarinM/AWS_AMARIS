def validate_schema(df, required_columns):
    """Check if all required columns exist in the DataFrame."""
    return all(col in df.columns for col in required_columns)
