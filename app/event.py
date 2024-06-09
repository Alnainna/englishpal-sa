from dataclasses import dataclass

class Event:
    pass


@dataclass
class NewWordAdded(Event):
    word: str

if __name__ == '__main__':
    event = NewWordAdded('architecture')





