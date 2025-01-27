# Student Performance Analytics Dashboard

This project visualizes and analyzes quiz performance data using a Streamlit-based dashboard. It incorporates three datasets: `Quiz_Endpoint.json`, `API_Endpoint.json`, and `Quiz_Submission_Data.json`, alongside a `json_conversion.py` script to structure unstructured data into a standardized format for analysis.

## Features
1. **Data Loading and Transformation**:
   - Includes `json_conversion.py` to convert unstructured data into a structured JSON format.
   - Processes three datasets for comprehensive analysis:
     - `Quiz_Endpoint.json`: Current quiz details.
     - `API_Endpoint.json`: Historical quiz performance data.
     - `Quiz_Submission_Data.json`: Question-level performance details.

2. **Interactive Dashboard**:
   - Displays student performance metrics, topic-wise analysis, and personalized recommendations.
   - Categorizes topics into strong, moderate, and weak categories with visual indicators.
   - Provides a radar chart for topic performance and a line chart for historical trends.

3. **Visual Enhancements**:
   - Custom CSS for highlighting topic categories.
   - Interactive charts built using Plotly.

---

## Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Required Python libraries:
  ```bash
  pip install streamlit pandas numpy plotly
  ```

---

## File Structure
```
|-- app.py                 # Main Streamlit application
|-- json_conversion.py     # Script to preprocess and structure unstructured data
|-- Quiz_Endpoint.json     # Current quiz data
|-- API_Endpoint.json      # Historical performance data
|-- Quiz_Submission_Data.json  # Question-level data
```

---

## Step-by-Step Guide

### 1. Convert Unstructured Data
Run the `json_conversion.py` script to preprocess and convert raw data into structured JSON format.

```bash
python json_conversion.py
```
Ensure the converted files (`Quiz_Endpoint.json`, `API_Endpoint.json`, and `Quiz_Submission_Data.json`) are placed in the same directory as `app.py`.

### 2. Run the Streamlit Dashboard
Launch the Streamlit application to visualize the data.

```bash
streamlit run app.py
```

### 3. Explore the Dashboard
The dashboard provides the following sections:

#### a. **Overall Performance**
Displays key performance metrics:
- Average score
- Average accuracy
- Total questions attempted
- Correct answers

#### b. **Topic-wise Analysis**
Analyzes topics with:
- **Radar Chart**: Accuracy across topics.
- **Topic Categories**: Topics grouped into strong (≥80%), moderate (60-79%), and weak (<60%) categories.

#### c. **Performance Trend**
A line chart showing accuracy trends over time.

#### d. **Detailed Topic Analysis**
A table summarizing accuracy, score, and attempts per topic.

#### e. **Personalized Recommendations**
Actionable insights to improve performance, categorized by topic.

---

## Example Data
### Quiz_Endpoint.json
Contains the details of the current quiz.
```json
{
  "quiz": {
    "title": "Structural Organisation in Animals",
    "topic": "Biology",
    "questions_count": 10,
    "correct_answers": 7,
    "incorrect_answers": 3,
    "score": 28,
    "accuracy": "70%"
  }
}
```

### API_Endpoint.json
Contains historical performance data.
```json
[
  {
    "quiz_id": 1,
    "score": 20,
    "accuracy": "66.67%",
    "submitted_at": "2024-01-20T14:30:00.000+00:00",
    "total_questions": 15,
    "correct_answers": 10,
    "incorrect_answers": 5,
    "quiz": {
      "topic": "Biology",
      "title": "Photosynthesis"
    }
  }
]
```

### Quiz_Submission_Data.json
Contains question-level details.
```json
{
  "quiz": {
    "questions": [
      {
        "id": 101,
        "description": "What is the powerhouse of the cell?",
        "topic": "Biology",
        "is_correct": true,
        "difficulty_level": "Easy"
      },
      {
        "id": 102,
        "description": "Define osmosis.",
        "topic": "Biology",
        "is_correct": false,
        "difficulty_level": "Medium"
      }
    ]
  }
}
```

---

## Key Insights
- **Flexible Analysis**: Combines multiple datasets to offer comprehensive insights into student performance.
- **Personalized Recommendations**: Provides targeted improvement suggestions based on weak areas.

---

## Future Enhancements
- Include additional visualizations for question-level insights.
- Support multiple students for batch performance analysis.

---

Feel free to reach out if you encounter issues or have suggestions for improvement!

