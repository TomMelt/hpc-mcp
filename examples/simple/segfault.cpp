#include <chrono>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <thread>

void decoyFunction3() {
  // This function does nothing but serves as a decoy
  std::cout << "Number is greater than 75. Crashing the program..."
            << std::endl;
  int *ptr = nullptr;
  *ptr = 42; // Dereferencing a null pointer to cause a crash
  return;
}

void decoyFunction2() {
  // This function does nothing but serves as a decoy
  return decoyFunction3();
}

void decoyFunction() {
  // This function does nothing but serves as a decoy
  return decoyFunction2();
}

int main() {
  // Seed the random number generator
  std::srand(std::time(0));

  // Generate a random number between 0 and 99
  int randomNumber = std::rand() % 100;

  std::cout << "Generated number: " << randomNumber << std::endl;

  decoyFunction(); // Call the decoy function

  // Sleep for 1 second
  // std::this_thread::sleep_for(std::chrono::seconds(1));

  // Crash the program if the number is greater than 75
  // if (randomNumber > 75) {
  // }

  std::cout << "Program completed successfully." << std::endl;
  return 0;
}
