# Option Pricing Models
Inspired by the knowledge I gained from Akuna Capital's Options 101 course, I embarked on creating this application. It is designed to price options through various models and provide visual representations such as heatmaps and payoff diagrams, applying the theoretical knowledge acquired in a practical, user-friendly tool.

This project is a comprehensive toolkit for pricing financial options using various models. It leverages Python libraries such as Streamlit, Pandas, Numpy, and Matplotlib to provide an interactive web application for quantitative financial analysis. Users can select between different pricing models, input parameters, and visualize the results through intuitive graphs and heatmaps.

## Features

- **Interactive Web Interface**: Built with Streamlit, offering a user-friendly interface for model selection and parameter input.
- **Support for Multiple Models**: Includes implementations for American options (Binomial model) and European options (Black-Scholes and Monte Carlo simulations).
- **Visualization Tools**: Utilizes Matplotlib and Seaborn for generating payoff diagrams and heatmaps, aiding in the analysis of option strategies.

## Installation

To set up the project environment, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python 3.6 or later installed.
3. Install the required dependencies by running:

```sh
pip install -r requirements.txt
```

## Usage

To run the application, execute the following command in the project's root directory:

```sh
streamlit run main.py
```

Navigate to the URL provided by Streamlit in your web browser to interact with the application.

## Models Supported

- **American Options**: Priced using the Binomial model.
- **European Options**: Priced using the Black-Scholes model and Monte Carlo simulations.

## Visualization

- **Payoff Diagrams**: Generate payoff diagrams for long/short calls and puts.
- **Heatmaps**: Visualize how different parameters affect the option's price.

## Database Integration

The application will be integrated with Supabase for data persistence, allowing users to store and retrieve input parameters.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Nikita Berezyuk, for the initial creation and maintenance of the project.
- The open-source community, for the libraries and tools that made this project possible.

## Contact

For any inquiries or contributions, please contact Nikita Berezyuk through [LinkedIn](https://www.linkedin.com/in/nikita-berezyuk/).