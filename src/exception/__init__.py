import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extracts detailed information includes file name , line number , and the error message
    :param error: The exception object .
    :param error_detail: The sys module to access the traceback information.
    : return A formatted string containing the error message, file name, and line number.
    """
    _,_, exc_tb = error_detail.exc.info()
    # exc.info give 3 things 1, type of error 2- error object itself 3 traceback object
    #but we need only traceback object to extract file name and line number

    file_name = exc.tb.tb_frame.f_code.co_filename
    # this gets which python file caused the error 

    line_number = exc_tb.tb_lineno
    # this gets exact line number where the error occurred

    error_message = f"Error occurred in python script: [{file_name}] at line number [{line_number}]: {str(error)}"
    ## Create a formatted error message string with file name, line number, and the actual error

    logging.error(error_message)
    #this logs/store the error 

    return error_message


class MyException(Exception):
    """
    Creating custom exception class that inherits from the built-in Exception class. This allows us to create our own exceptions with custom behavior.
    """
    def __init__ (self, error_message: str , error_detail: sys):
        """
        Runs Automatically when an instance of Myexception is created . It initializes the exception with a detailed error message that includes the file name and line number where the error occurred. It also logs the error message for debugging purposes.
        Intialize the USVisa Exception with a detailed error message.
        :param error_message: The error message to be associated with the exception.
        :param error_detail: The sys module to access the traceback information for detailed error context.

        """
        #Call the base class constructor with the error message 
        super().__init__(error_message)
        #call the base class constuructor to initialize the exception with the provided error message

        self.error_message = error_message_detail(error_message, error_detail)
        # Format the detailed error message using the error message and error details, and store it in the instance variable self.error_message

        def __str__(self):
            """
            This controls what prints when exception is shown.
            :return: The string representation of the error message.

            """
            return self.error_message

