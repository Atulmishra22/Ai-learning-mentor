from mentor.database.init_db import init_db
from mentor.llm import get_response


def main():
    init_db()
    
if __name__ == "__main__":
    main()
