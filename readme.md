# KeyPassAI

KeyPassAI is an intelligent password manager built using Python, PyQt5 for the graphical interface, and OpenAI's GPT-4o for password generation and analysis. This application helps users securely store, generate, and analyze passwords with the assistance of AI.

## Features

- **Secure Password Storage:** Store passwords securely with encryption.
- **Password Generation:** Generate secure passwords using AI (GPT-4o).
- **Password Analysis:** Analyze the security of passwords using AI (GPT-4o).
- **User-Friendly Interface:** Intuitive interface for easy password management.
- **Account Management:** Save and load account details for various services.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/king-tri-ton/keypassai.git
    cd keypassai
    ```

2. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the configuration:**

    - Obtain an API key from OpenAI and update the `AI_TOKEN` variable in `config.py`.
    - Rename `exp.config.py` to `config.py`.

    ```bash
    mv exp.config.py config.py
    ```

4. **Run the application:**

    ```bash
    python app.py
    ```

## Usage

1. **Generate a Password:**
   - Click the "Generate Password" button to create a secure password using AI (GPT-4o).

2. **Save a Password:**
   - Fill in the service name, username, and password fields, then click "Save Password" to securely store your credentials.

3. **Analyze a Password:**
   - Enter a password and click "Analyze Password" to get an AI-driven security analysis using GPT-4o.

4. **Load Accounts:**
   - Click "Load Accounts" to view all saved accounts. Click on an account to load its details.

## File Structure

- `app.py`: Main application code.
- `config.py`: Configuration file containing sensitive information like the OpenAI API key.
- `requirements.txt`: List of dependencies required to run the application.

## Security Notes

1. **API Token:** Ensure that your OpenAI API token is kept confidential.
2. **Encryption Key:** The encryption key is currently stored in a file named `secret.key`. This is a security risk, and future updates will address more secure key management solutions.

## Future Updates

We are committed to improving the security of KeyPassAI. Future updates will focus on:
- Enhanced key management to protect encryption keys.
- Additional security measures for storing and accessing sensitive data.
- Continuous improvement of AI-driven password generation and analysis using GPT-4o.

## Requirements

- Python 3.x
- PyQt5
- Cryptography
- OpenAI API

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact [mdolmatov99@gmail.com](mailto:mdolmatov99@gmail.com) or reach out on [Telegram](https://t.me/king_triton).

---

Feel free to reach out if you encounter any issues or have suggestions for improvements. Happy password managing with KeyPassAI!
