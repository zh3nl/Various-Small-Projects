import random

dice_counter = 0

while True:
    choice = input("Roll the dice? (y/n): ").lower()

    if choice == "y":
        num_rolls = int(input("How many dice do you want to roll? "))

        dice_counter += num_rolls

        for roll in range(num_rolls):
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            print(f'({die1}, {die2})')

        print(f'Total rolls: {dice_counter}')
    elif choice == "n":
        print("Thanks for playing!")
        break
    else:
        print("Invalid choice!")
