def mad_libs():
    print("Welcome to the Mad Libs game!")
    

    adjective1 = input("Enter an adjective: ")
    noun1 = input("Enter a noun: ")
    verb1 = input("Enter a verb: ")
    adverb1 = input("Enter an adverb: ")
    noun2 = input("Enter another noun: ")
    

    story = f"Once upon a time, there was a {adjective1} {noun1} that loved to {verb1} {adverb1}. " \
            f"One day, it met a {noun2} and they became the best of friends."
    
    # Print
    print("\nHere's your Mad Libs story:")
    print(story)

# Run 
mad_libs()
