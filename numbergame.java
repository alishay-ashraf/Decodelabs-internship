import java.util.Random;
import java.util.Scanner;

public class NumberGame {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();
        
        // Game configuration
        int minRange = 1;
        int maxRange = 100;
        int maxAttempts = 7; // Optional Enhancement: Limit the number of attempts
        
        int totalRounds = 0;
        int totalScore = 0; // Optional Enhancement: Display final score
        boolean playAgain = true;

        System.out.println(" Welcome to the Number Guessing Game!");
        System.out.println("I'm thinking of a number between " + minRange + " and " + maxRange + ".");
        System.out.println("You have " + maxAttempts + " attempts per round. Good luck!\n");

        // Optional Enhancement: Allow multiple rounds using a loop
        while (playAgain) {
            totalRounds++;
            // Key Requirement: Generate a random number
            int targetNumber = random.nextInt(maxRange - minRange + 1) + minRange;
            int attempts = 0;
            boolean wonRound = false;

            System.out.println("--- Round " + totalRounds + " ---");

            // Loop for handling user attempts within a single round
            while (attempts < maxAttempts) {
                System.out.print("Enter your guess (Attempt " + (attempts + 1) + "/" + maxAttempts + "): ");
                
                // Input validation to check if user entered an integer
                if (!scanner.hasNextInt()) {
                    System.out.println("Invalid input. Please enter a valid number.");
                    scanner.next(); // Clear the invalid input
                    continue;
                }

                // Key Requirement: Take user input for guesses
                int userGuess = scanner.nextInt();
                attempts++;

                // Key Requirement: Provide feedback if the guess is too high or too low
                if (userGuess == targetNumber) {
                    System.out.println("🎉 Correct! You guessed the number in " + attempts + " attempts.");
                    // Score calculation: higher score for fewer attempts
                    int roundScore = (maxAttempts - attempts + 1) * 10;
                    totalScore += roundScore;
                    System.out.println("Round Score: " + roundScore + " points.");
                    wonRound = true;
                    break; // Exit the attempt loop
                } else if (userGuess < targetNumber) {
                    System.out.println("Too low! Try a higher number.");
                } else {
                    System.out.println("Too high! Try a lower number.");
                }
            }

            if (!wonRound) {
                System.out.println("😢 Out of attempts! The correct number was: " + targetNumber);
            }

            // Ask user if they want to play another round
            System.out.print("\nDo you want to play another round? (yes/no): ");
            String response = scanner.next().trim().toLowerCase();
            if (!response.equals("yes") && !response.equals("y")) {
                playAgain = false;
            }
            System.out.println();
        }

        // Optional Enhancement: Display the final score and summary
        System.out.println("====================================");
        System.out.println("            GAME OVER               ");
        System.out.println("====================================");
        System.out.println("Total Rounds Played: " + totalRounds);
        System.out.println("Final Score:         " + totalScore + " points");
        System.out.println("Thanks for playing! Goodbye!");

        scanner.close();
    }
}