import sys; sys.dont_write_bytecode = True
from chatgptapibypass.core import *

def main():
    response = chatgpt(
        "Simply explain quantum physics",
        search=True 
    )
    
    if response:
        print("\nChatGPT Response:")
        print(response)
        input("Press Enter to exit...")
    else:
        print("Failed to get response")

if __name__ == "__main__":
    main()
    os._exit(0)