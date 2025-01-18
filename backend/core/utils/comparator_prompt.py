import json

def generate_comparison_prompt(new_product, competitor_list):
    """
    Generates a comparison prompt for the Gemini API.

    Args:
        new_product: Dictionary representing the new product.
        competitor_list: List of dictionaries representing competitors.

    Returns:
        A string containing the comparison prompt.
    """

    prompt = f"""
    Compare the following products:

    New Product: {json.dumps(new_product)}
    Competitors: {json.dumps(competitor_list)}

    Identify the key advantages and unique selling propositions of the New Product 
    compared to its competitors. 
    """

    return prompt