# JobCMD - Resume Evaluation Chatbot

**JobCMD** is a Streamlit-powered chatbot that uses Google Generative AI (Gemini model) to analyze resumes and compare them with job descriptions. The application helps HR professionals and job seekers by providing detailed feedback on resume alignment with job roles and calculates the percentage match between the resume and job description.

## Features

- **Resume Evaluation**: Evaluates how well a resume aligns with the job description, highlighting strengths and weaknesses.
- **Percentage Match**: Calculates the percentage match between the resume and job description, listing missing keywords.
- **Keyword Extraction**: Extracts and displays relevant keywords from the job description and resume.
- **User-Friendly UI**: Modern, responsive design with color-coded sections and progress indicators.

## Technologies Used

- **Streamlit**: Framework for creating interactive web applications in Python.
- **Google Generative AI (Gemini model)**: AI model for generating and analyzing text content.
- **PyMuPDF (fitz)**: Library for reading and extracting text from PDF files.
- **Python**: Programming language used for implementing the core functionalities.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/JobCMD.git](https://github.com/Itzkuldeep/JodCmd.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd JobCMD
    ```

3. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Create a `.env` file** in the root directory with your Google API key:
    ```plaintext
    GOOGLE_API_KEY=your_google_api_key_here
    ```

6. **Run the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

## Usage

1. **Upload a Resume**: Use the file uploader to upload a PDF resume.
2. **Enter Job Description**: Paste the job description in the provided text area.
3. **Evaluate Resume**: Click the "Evaluate Resume" button to get feedback on the resume.
4. **Get Percentage Match**: Click the "Percentage Match" button to see how well the resume matches the job description.
5. **Extract Skills**: Click the "Extract Skills" button to view matched keywords.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes.
4. Push your changes to the forked repository.
5. Create a pull request with a description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
