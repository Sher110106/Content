import json
import operator

def basic_calculator(input_str):
    """
    Perform a numeric operation on two numbers based on the input string or dictionary.

    Parameters:
    input_str (str or dict): Either a JSON string representing a dictionary with keys
                             or a dictionary directly. Example: '{"num1": 5, "num2": 3, "operation": "add"}'
    
    Returns:
    str: The formatted result of the operation.

    Raises:
    Exception: If an error occurs during the operation (e.g., division by zero).
    ValueError: If an unsupported operation is requested or input is invalid.
    """
    try:
        # Handle both dictionary and string inputs
        if isinstance(input_str, dict):
            input_dict = input_str
        else:
            # Clean and parse the input string
            input_str_clean = input_str.replace("'", "\"").strip().strip("\"")
            input_dict = json.loads(input_str_clean)

        # Validate required fields
        if not all(key in input_dict for key in ['num1', 'num2', 'operation']):
            return "Error: Input must contain 'num1', 'num2', and 'operation'"

        num1 = float(input_dict['num1'])
        num2 = float(input_dict['num2'])
        operation = input_dict['operation'].lower()

    except (json.JSONDecodeError, KeyError):
        return "Invalid input format. Please provide valid numbers and operation."
    except ValueError:
        return "Error: Please provide valid numerical values."

    # Define supported operations
    operations = {
        'add': operator.add,
        'plus': operator.add,
        'subtract': operator.sub,
        'minus': operator.sub,
        'multiply': operator.mul,
        'times': operator.mul,
        'divide': operator.truediv,
        'floor_divide': operator.floordiv,
        'modulus': operator.mod,
        'power': operator.pow,
        'lt': operator.lt,
        'le': operator.le,
        'eq': operator.eq,
        'ne': operator.ne,
        'ge': operator.ge,
        'gt': operator.gt
    }

    if operation not in operations:
        return f"Unsupported operation: '{operation}'. Supported operations are: {', '.join(operations.keys())}"

    try:
        if operation in ['divide', 'floor_divide', 'modulus'] and num2 == 0:
            return "Error: Division by zero is not allowed"

        result = operations[operation](num1, num2)

        if isinstance(result, bool):
            result_str = "True" if result else "False"
        elif isinstance(result, float):
            result_str = f"{result:.6f}".rstrip('0').rstrip('.')  # Trim trailing zeros and dot
        else:
            result_str = str(result)

        return f"The answer is: {result_str}"

    except Exception as e:
        return f"Error during calculation: {str(e)}"


def reverse_string(input_string):
    """
    Reverse the given string.

    Parameters:
    input_string (str): The string to be reversed.

    Returns:
    str: The reversed string.
    """
    if not isinstance(input_string, str):
        return "Error: Input must be a string"
    
    reversed_string = input_string[::-1]
    return f"The reversed string is: {reversed_string}"
