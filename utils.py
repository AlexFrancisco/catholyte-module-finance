import os
from flask import current_app
from app.services.llm_service import generate_llm_content, construct_prompt

def categorize_transaction(transaction_description):
    """
    Categorizes a transaction using the LLM service.

    Args:
        transaction_description (str): The description of the transaction.

    Returns:
        str: The category of the transaction, as determined by the LLM.
    """
    prompt = construct_prompt("transaction_categorization", transaction_description=transaction_description)
    model = current_app.config.get("DEFAULT_LLM_MODEL", "granite3.2:8b")
    category = generate_llm_content(model=model, prompt=prompt)
    return category