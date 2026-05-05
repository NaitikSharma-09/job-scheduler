import random

print("Hello bitches! ")
print("Enter Your name:")
name = input()
print("Hello ",name)
random_letter = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
chosen_letter = random.choice(random_letter)
print("Your random letter is:", chosen_letter)