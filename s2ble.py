from core import braille
from utils.typer import Typer

def main():
    print("starting typer")
    print("esc to quit")
    typer = Typer(braille.Encoding("s2b/en_english.s2b"))

if __name__ == "__main__":
    main()