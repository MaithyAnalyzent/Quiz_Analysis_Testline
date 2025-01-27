import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os


st.set_page_config(layout="wide", page_title="Student Performance Analytics")


st.markdown("""
    <style>
    .topic-card {
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .strong {
        background-color: #F45786;
        border: 1px solid #c3e6cb;
    }
    .moderate {
        background-color: #BF72FD;
        border: 1px solid #ffeeba;
    }
    .weak {
        background-color: #48A4FA;
        border: 1px solid #f5c6cb;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


def load_data():
    try:
        if not os.path.exists('Quiz_Endpoint.json'):
            st.error("Quiz_Endpoint.json file not found.")
            return None, None
        with open('Quiz_Endpoint.json', 'r') as f:
            current_quiz_data = json.load(f)
        if not os.path.exists('API_Endpoint.json'):
            st.error("API_Endpoint.json file not found.")
            return None, None
        with open('API_Endpoint.json', 'r') as f:
            historical_data = json.load(f)
        return current_quiz_data, historical_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None


def process_current_quiz_data(data):
    quiz_details = data['quiz']
    summary = {
        'Quiz Title': quiz_details.get('title', 'N/A'),
        'Topic': quiz_details.get('topic', 'N/A'),
        'Total Questions': quiz_details.get('questions_count', 0),
        'Correct Answers': data.get('correct_answers', 0),
        'Incorrect Answers': data.get('incorrect_answers', 0),
        'Score': data.get('score', 0),
        'Accuracy': data.get('accuracy', 'N/A'),
    }
    return summary


def process_historical_data(data):
    quiz_records = []
    for record in data:
        quiz_records.append({
            'quiz_id': record['quiz_id'],
            'score': record['score'],
            'accuracy': float(record['accuracy'].strip('%')),
            'submitted_at': datetime.strptime(record['submitted_at'], '%Y-%m-%dT%H:%M:%S.%f%z'),
            'total_questions': record['total_questions'],
            'correct_answers': record['correct_answers'],
            'incorrect_answers': record['incorrect_answers'],
            'topic': record['quiz']['topic'] if record['quiz']['topic'] else 'Unknown',
            'title': record['quiz']['title'],
            'duration': record['duration']
        })

    df = pd.DataFrame(quiz_records)
    topic_performance = df.groupby('topic').agg({
        'accuracy': 'mean',
        'score': 'mean',
        'quiz_id': 'count'
    }).round(2)
    return df, topic_performance


def categorize_topics(topic_performance):
    strong_topics = topic_performance[topic_performance['accuracy'] >= 80].index.tolist()
    moderate_topics = topic_performance[(topic_performance['accuracy'] >= 60) & 
                                     (topic_performance['accuracy'] < 80)].index.tolist()
    weak_topics = topic_performance[topic_performance['accuracy'] < 60].index.tolist()
    
    return strong_topics, moderate_topics, weak_topics


def display_topic_category(title, topics, style_class):
    if topics:
        st.markdown(f"""
            <div class="topic-card {style_class}">
                <h4>{title}</h4>
                <ul>
                    {''.join([f'<li>{topic}</li>' for topic in topics])}
                </ul>
            </div>
        """, unsafe_allow_html=True)


def create_radar_chart(topic_performance):
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=topic_performance['accuracy'],
        theta=topic_performance.index,
        fill='toself',
        name='Accuracy'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False
    )
    
    return fig

def define_student_persona(performance_df):
    mean_accuracy = performance_df['accuracy'].mean()
    if mean_accuracy >= 80:
        return "High Achiever: Consistently performs well across topics."
    elif mean_accuracy >= 60:
        return "Balanced Learner: Performs well in some areas but has room for improvement in others."
    else:
        return "Needs Improvement: Focused effort required to improve overall performance."

def main():
    st.title("🎯 Student Performance Analytics Dashboard")

    # Load data
    current_quiz_data, historical_data = load_data()

    if not current_quiz_data or not historical_data:
        st.error("Failed to load data. Ensure both JSON files are in the directory.")
        return

    current_summary = process_current_quiz_data(current_quiz_data)
    performance_df, topic_performance = process_historical_data(historical_data)
    

    st.sidebar.header("📊 Dashboard Info")
    st.sidebar.markdown(f"""
        - **Total Quizzes Attempted**: {len(performance_df)}
        - **Time Period**: {performance_df['submitted_at'].min().date()} to {performance_df['submitted_at'].max().date()}
        - **Topics Covered**: {len(performance_df['topic'].unique())}
    """)
    

    st.header("📈 Overall Performance")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Score", f"{performance_df['score'].mean():.1f}")
    with col2:
        st.metric("Average Accuracy", f"{performance_df['accuracy'].mean():.1f}%")
    with col3:
        st.metric("Total Questions", performance_df['total_questions'].sum())
    with col4:
        st.metric("Correct Answers", performance_df['correct_answers'].sum())
    

    st.header("📚 Topic-wise Analysis")
    

    col1, col2 = st.columns([2, 1])
    
    with col1:
        
        st.subheader("Topic Performance Radar")
        radar_fig = create_radar_chart(topic_performance)
        st.plotly_chart(radar_fig, use_container_width=True)
    
    with col2:

        st.subheader("Topic Categories")
        strong_topics, moderate_topics, weak_topics = categorize_topics(topic_performance)
        
        display_topic_category("💪 Strong Topics (≥80%)", strong_topics, "strong")
        display_topic_category("👍 Moderate Topics (60-79%)", moderate_topics, "moderate")
        display_topic_category("📝 Topics Needing Focus (<60%)", weak_topics, "weak")
    
    # Performance Trend
    st.header("📊 Performance Trend")
    trend_fig = px.line(performance_df.sort_values('submitted_at'), 
                       x='submitted_at', 
                       y='accuracy',
                       title='Accuracy Trend Over Time',
                       labels={'submitted_at': 'Date', 'accuracy': 'Accuracy (%)'},
                       markers=True)
    trend_fig.update_traces(line_color='#2E86C1')
    st.plotly_chart(trend_fig, use_container_width=True)

    st.header("📋 Detailed Topic Analysis")
    detailed_df = topic_performance.copy()
    detailed_df.columns = ['Average Accuracy (%)', 'Average Score', 'Number of Attempts']
    st.dataframe(detailed_df, use_container_width=True)
    

    st.header("🎯 Personalized Recommendations")
    if weak_topics:
        st.warning(f"Focus on improving: {', '.join(weak_topics)}")
        st.markdown("- Consider dedicating more practice time to these topics")
        st.markdown("- Review fundamental concepts in these areas")
    
    if moderate_topics:
        st.info(f"Continue practicing: {', '.join(moderate_topics)}")
        st.markdown("- Work on improving accuracy in these topics")
        st.markdown("- Try attempting more challenging questions")
    
    if strong_topics:
        st.success(f"Maintain performance in: {', '.join(strong_topics)}")
        st.markdown("- Challenge yourself with advanced problems")
        st.markdown("- Consider helping peers in these topics")

    st.sidebar.header("Student Persona")
    persona = define_student_persona(performance_df)
    st.sidebar.markdown(f"**{persona}**")

if __name__ == "__main__":
    main()