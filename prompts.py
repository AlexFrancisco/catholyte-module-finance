FINANCE_PROMPTS = {
    "transaction_categorization": """
    You are a financial expert. Categorize the following transaction into one of these categories:
    - Groceries
    - Dining
    - Entertainment
    - Travel
    - Utilities
    - Rent
    - Salary
    - Investments
    - Other

    Transaction Description: {{transaction_description}}
    Category:
    """
}