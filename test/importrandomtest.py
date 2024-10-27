import random
from randomtest import bag

def main():
    marble_r = bag([0, 1, 2, 3])

    for i in range(10):
        print(marble_r.draw)

if __name__ == "__main__":
    main()
    
