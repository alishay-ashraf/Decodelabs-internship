import java.util.Scanner;

public class GradeCalculator {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("=== STUDENT GRADE CALCULATOR ===");
        
        // 1. Take the number of subjects
        System.out.print("Enter the number of subjects: ");
        int numSubjects = scanner.nextInt();
        
        // Validate input
        if (numSubjects <= 0) {
            System.out.println("Invalid number of subjects. Exiting program.");
            return;
        }

        int[] marks = new int[numSubjects];
        int totalMarks = 0;

        // 2. Loop to take marks for each subject
        for (int i = 0; i < numSubjects; i++) {
            while (true) {
                System.out.print("Enter marks for Subject " + (i + 1) + " (out of 100): ");
                int inputMark = scanner.nextInt();

                // Validate that marks are between 0 and 100
                if (inputMark >= 0 && inputMark <= 100) {
                    marks[i] = inputMark;
                    totalMarks += inputMark; // Accumulate total marks
                    break; // Exit the validation loop
                } else {
                    System.out.println("Invalid input! Marks must be between 0 and 100. Try again.");
                }
            }
        }

        // 3. Calculate average percentage
        // Using double to preserve decimal precision
        double averagePercentage = (double) totalMarks / numSubjects;

        // 4. Assign grades based on percentage using conditional statements (if-else)
        char grade;
        if (averagePercentage >= 90) {
            grade = 'A';
        } else if (averagePercentage >= 80) {
            grade = 'B';
        } else if (averagePercentage >= 70) {
            grade = 'C';
        } else if (averagePercentage >= 60) {
            grade = 'D';
        } else if (averagePercentage >= 50) {
            grade = 'E';
        } else {
            grade = 'F';
        }

        // 5. Display results clearly
        System.out.println("\n=============================");
        System.out.println("          RESULTS            ");
        System.out.println("=============================");
        System.out.println("Total Marks Obtained : " + totalMarks + " / " + (numSubjects * 100));
        System.out.printf("Average Percentage   : %.2f%%\n", averagePercentage);
        System.out.println("Assigned Grade       : " + grade);
        System.out.println("=============================");

        scanner.close();
    }
}