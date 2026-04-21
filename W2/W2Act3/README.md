# Powerxy Calculator

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/eirikrbe/MSE800-PSD)

This program calculates the power of a given base raised to an exponent. It includes input validation to ensure valid numbers are accepted and allows the user to interact with the app.

## Features

- Interactive user input for base and exponent.
- Error handling for invalid (non-numeric) inputs.
- Validation to reject undefined cases (0 raised to a non-positive exponent).
- Loop-based retry on invalid input.
- Option to continue calculations or exit.

### Screenshot

![Powerxy Calculator screenshot](powerxy-screenshot.png)

### Example Interaction

```
Enter the Base: 0
Enter the Exponent: -1
Undefined: 0 cannot be raised to a non-positive exponent.
Enter the Base: 2
Enter the Exponent: 3
2.0 raised to the power of 3.0 is 8.0
Do you want to continue? (y/n): y
Enter the Base: 1.5
Enter the Exponent: -2
1.5 raised to the power of -2.0 is 0.4444444444444444
Do you want to continue? (y/n): n
Program finished.
```

## Environment

- Python 3.x
- Anaconda (Custom environment "W1Env 3.8.20")
- Visual studio code