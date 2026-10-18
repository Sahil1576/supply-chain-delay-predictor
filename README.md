# Supply Chain Delay Predictor

An AI-powered application that predicts supply chain delays using Machine Learning and generates detailed reports using an LLM.

## Features

- Predict shipment delays using a trained Machine Learning model.
- Upload CSV datasets for analysis.
- Analyze missing values, duplicate rows, and dataset statistics.
- Evaluate model performance using accuracy, classification report, and confusion matrix.
- Identify important features affecting predictions.
- Generate AI-powered reports with possible delay reasons and recommendations.

## Tech Stack

- Python
- Pandas
- Scikit-learn
- FastAPI
- LangChain
- Groq LLM
- HTML, CSS, JavaScript

## Project Structure

```text
supply-chain-delay-predictor/
├── frontend/
├── LLM/
├── model/
├── report_generator/
├── main.py
├── pyproject.toml
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/supply-chain-delay-predictor.git
cd supply-chain-delay-predictor
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -e .
```

4. Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

## Usage

1. Start the application using the appropriate entry point.
2. Upload a CSV dataset containing the required features.
3. Generate shipment delay predictions and dataset analysis.
4. Get an AI-generated report with insights and recommendations.

## Important Notes

- Use a dataset with the features expected by the trained model.
- Model evaluation metrics require actual target labels.
- Keep API keys and other secrets out of version control.
- Do not upload sensitive datasets or credentials to GitHub.

## Future Improvements

- Interactive prediction dashboard.
- SHAP-based explanations.
- Better model evaluation and monitoring.
- Deployment as a web application.

## License

This project is available for educational and learning purposes.
