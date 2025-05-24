import os
from flask import current_app
from app.core.services import generate_content, construct_prompt, DEFAULT_MODEL

def categorize_transaction(transaction_description):
    """
    Categorizes a transaction using the LLM service.

    Args:
        transaction_description (str): The description of the transaction.

    Returns:
        str: The category of the transaction, as determined by the LLM.
    """
    FINANCE_PROMPTS = {
        "transaction_categorization": "Categorize the following transaction description into one of these categories (e.g., Groceries, Utilities, Entertainment, Income, Transfer, Other): {input_text}"
    }

    prompt_text_for_llm = construct_prompt(
        prompt_type="transaction_categorization",
        input_text=transaction_description,
        prompt_templates=FINANCE_PROMPTS
    )

    if not prompt_text_for_llm:
        current_app.logger.error("Failed to construct prompt for transaction categorization.")
        return "Error: Prompt construction failed"

    model_to_use = current_app.config.get("DEFAULT_LLM_MODEL", DEFAULT_MODEL)

    response_data = generate_content(
        model_name=model_to_use,
        prompt_type="transaction_categorization",
        input_text=transaction_description,
        prompt_templates=FINANCE_PROMPTS
    )
    
    category = response_data.get("response", "Uncategorized")
    if response_data.get("error"):
        current_app.logger.error(f"LLM error categorizing transaction: {response_data.get('error')}")
        return f"Error: {response_data.get('error')}"
        
    return category.strip() if category else "Uncategorized"